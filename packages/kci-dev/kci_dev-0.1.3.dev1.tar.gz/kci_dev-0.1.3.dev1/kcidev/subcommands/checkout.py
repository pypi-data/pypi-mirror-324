#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import re
import subprocess
import sys
import time

import click
import requests
from git import Repo

from kcidev.libs.common import *
from kcidev.libs.maestro_common import *


def send_checkout_full(baseurl, token, **kwargs):
    url = baseurl + "api/checkout"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"{token}",
    }
    data = {
        "url": kwargs["giturl"],
        "branch": kwargs["branch"],
        "commit": kwargs["commit"],
        "jobfilter": kwargs["job_filter"],
    }
    if "platform_filter" in kwargs:
        data["platformfilter"] = kwargs["platform_filter"]
    jdata = json.dumps(data)
    maestro_print_api_call(url, data)
    try:
        response = requests.post(url, headers=headers, data=jdata, timeout=30)
    except requests.exceptions.RequestException as e:
        kci_err(f"API connection error: {e}")
        return None

    if response.status_code != 200:
        maestro_api_error(response)
        return None
    return response.json()


def retrieve_treeid_nodes(baseurl, token, treeid):
    url = baseurl + "latest/nodes/fast?treeid=" + treeid
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"{token}",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        click.secho(f"API connection error: {e}, retrying...", fg="yellow")
        return None
    except Exception as e:
        click.secho(f"API connection error: {e}, retrying...", fg="yellow")
        return None

    if response.status_code >= 400:
        maestro_api_error(response)
        return None

    return response.json()


def check_node(node):
    """
    Node can be defined RUNNING/DONE/FAIL based on the state
    Simplify, as our current state model suboptimal
    """
    name = node["name"]
    state = node["state"]
    result = node["result"]
    if name == "checkout":
        if state == "running":
            return "RUNNING"
        elif state == "available" or state == "closing":
            return "DONE"
        elif state == "done" and result == "pass":
            return "DONE"
        else:
            return "FAIL"
    else:
        if state == "running":
            return "RUNNING"
        elif state == "done" and result == "pass":
            return "DONE"
        else:
            return "FAIL"


def watch_jobs(baseurl, token, treeid, job_filter, test):
    # we need to add to job_filter "checkout" node
    job_filter = list(job_filter)
    job_filter.append("checkout")
    previous_nodes = None
    while True:
        inprogress = 0
        joblist = job_filter.copy()
        nodes = retrieve_treeid_nodes(baseurl, token, treeid)
        if not nodes:
            click.secho("No nodes found. Retrying...", fg="yellow")
            time.sleep(5)
            continue
        if previous_nodes == nodes:
            kci_msg_nonl(".")
            time.sleep(30)
            continue

        time_local = time.localtime()
        click.echo(f"\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S', time_local)}")
        click.secho(
            f"Total tree nodes {len(nodes)} found. job_filter: {job_filter}", fg="green"
        )

        # Tricky part in watch is that we might have one item in job_filter (job, test),
        # but it might spawn multiple nodes with same name
        test_result = None
        jobs_done_ts = None
        for node in nodes:
            if node["name"] == test:
                test_result = node["result"]
            if node["name"] in job_filter:
                result = check_node(node)
                if result == "DONE":
                    if isinstance(joblist, list) and node["name"] in joblist:
                        joblist.remove(node["name"])
                    color = "green"
                elif result == "RUNNING":
                    inprogress += 1
                    color = "yellow"
                else:
                    if isinstance(joblist, list) and node["name"] in joblist:
                        joblist.remove(node["name"])
                    color = "red"
                    # if test is same as job, dont indicate infra-failure if test job fail
                    if test and test != node["name"]:
                        # if we have a test, and prior job failed, we should indicate that
                        kci_err(f"Job {node['name']} failed, test can't be executed")
                        sys.exit(2)
                nodeid = node.get("id")
                click.secho(
                    f"Node: {nodeid} job: {node['name']} State: {node['state']} Result: {node['result']}",
                    fg=color,
                )
        if len(joblist) == 0 and inprogress == 0:
            click.secho("All jobs completed", fg="green")
            if not test:
                return
            else:
                if not jobs_done_ts:
                    jobs_done_ts = time.time()
                # if all jobs done, usually test results must be available
                # max within 60s. Safeguard in case of test node is not available
                if not test_result and time.time() - jobs_done_ts < 60:
                    continue

                if test_result and test_result == "pass":
                    click.secho(f"Test {test} passed", fg="green")
                    sys.exit(0)
                elif test_result:
                    # ignore null, that means result not ready yet
                    kci_err(f"Test {test} failed: {test_result}")
                    sys.exit(1)

        kci_msg_nonl(f"\rRefresh every 30s...")
        previous_nodes = nodes
        time.sleep(30)


def retrieve_tot_commit(repourl, branch):
    """
    Retrieve the latest commit on a branch

    Unfortunately, gitpython does not support fetching the latest commit
    on a branch without having to clone the repo.
    """
    process = subprocess.Popen(
        ["git", "ls-remote", repourl, f"refs/heads/{branch}"], stdout=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    sha = re.split(r"\t+", stdout.decode("ascii"))[0]
    return sha


@click.command(help="Create custom tree checkout on KernelCI and trigger a tests")
@click.option(
    "--giturl",
    help="Git URL to checkout",
    required=True,
)
@click.option(
    "--branch",
    help="Branch to checkout",
    required=True,
)
@click.option(
    "--commit",
    help="Commit to checkout",
)
@click.option(
    "--tipoftree",
    help="Checkout on latest commit on tree/branch",
    is_flag=True,
)
@click.option(
    "--watch",
    "-w",
    help="Interactively watch for a tasks in job-filter",
    is_flag=True,
)
# job_filter is a list, might be one or more jobs
@click.option(
    "--job-filter",
    help="Job filter to trigger",
    multiple=True,
)
@click.option(
    "--platform-filter",
    help="Platform filter to trigger",
    multiple=True,
)
@click.option(
    "--test",
    help="Return code based on the test result",
)
@click.pass_context
def checkout(
    ctx, giturl, branch, commit, job_filter, platform_filter, tipoftree, watch, test
):
    cfg = ctx.obj.get("CFG")
    instance = ctx.obj.get("INSTANCE")
    url = cfg[instance]["pipeline"]
    apiurl = cfg[instance]["api"]
    token = cfg[instance]["token"]
    if not job_filter:
        job_filter = None
        click.secho("No job filter defined. All jobs will be triggered!", fg="yellow")
    if watch and not job_filter:
        kci_err("No job filter defined. Can't watch for a job(s)!")
        return
    if test and not watch:
        kci_err("Test option only works with watch option")
        return
    if not commit and not tipoftree:
        kci_err("No commit or tree/branch latest commit defined")
        return
    if tipoftree:
        click.secho(
            f"Retrieving latest commit on tree: {giturl} branch: {branch}", fg="green"
        )
        commit = retrieve_tot_commit(giturl, branch)
        if not commit or len(commit) != 40:
            kci_err("Unable to retrieve latest commit. Wrong tree/branch?")
            return
        click.secho(f"Commit to checkout: {commit}", fg="green")
    resp = send_checkout_full(
        url,
        token,
        giturl=giturl,
        branch=branch,
        commit=commit,
        job_filter=job_filter,
        platform_filter=platform_filter,
        watch=watch,
    )
    if not resp:
        kci_err("Failed to trigger checkout")
        sys.exit(64)

    if resp and "message" in resp:
        click.secho(resp["message"], fg="green")

    if watch and isinstance(resp, dict):
        node = resp.get("node")
        treeid = node.get("treeid")
        if not treeid:
            kci_err("No treeid returned. Can't watch for a job(s)!")
            return
        click.secho(f"Watching for jobs on treeid: {treeid}", fg="green")
        if test:
            click.secho(f"Watching for test result: {test}", fg="green")
        # watch for jobs
        watch_jobs(apiurl, token, treeid, job_filter, test)


if __name__ == "__main__":
    main_kcidev()

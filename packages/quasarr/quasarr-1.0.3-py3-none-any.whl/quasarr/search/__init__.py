# -*- coding: utf-8 -*-
# Quasarr
# Project by https://github.com/rix1337

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from quasarr.search.sources.dd import dd_search
from quasarr.search.sources.dw import dw_feed, dw_search
from quasarr.search.sources.fx import fx_feed, fx_search
from quasarr.search.sources.nx import nx_feed, nx_search
from quasarr.search.sources.sf import sf_feed, sf_search


def get_search_results(shared_state, request_from, search_string="", season="", episode=""):
    results = []

    dd = shared_state.values["config"]("Hostnames").get("dd")
    dw = shared_state.values["config"]("Hostnames").get("dw")
    fx = shared_state.values["config"]("Hostnames").get("fx")
    nx = shared_state.values["config"]("Hostnames").get("nx")
    sf = shared_state.values["config"]("Hostnames").get("sf")

    functions = []
    if search_string:
        if season and episode:
            search_string = f"{search_string} S{int(season):02}E{int(episode):02}"
        elif season:
            search_string = f"{search_string} S{int(season):02}"

        if dd:
            functions.append(lambda: dd_search(shared_state, search_string))
        if dw:
            functions.append(lambda: dw_search(shared_state, request_from, search_string))
        if fx:
            functions.append(lambda: fx_search(shared_state, search_string))
        if nx:
            functions.append(lambda: nx_search(shared_state, request_from, search_string))
        if sf:
            functions.append(lambda: sf_search(shared_state, request_from, search_string))
    else:
        if dd:
            functions.append(lambda: dd_search(shared_state))
        if dw:
            functions.append(lambda: dw_feed(shared_state, request_from))
        if fx:
            functions.append(lambda: fx_feed(shared_state))
        if nx:
            functions.append(lambda: nx_feed(shared_state, request_from))
        if sf:
            functions.append(lambda: sf_feed(shared_state, request_from))

    stype = f'search phrase "{search_string}"' if search_string else "feed search"
    print(f'Starting {len(functions)} search functions for {stype}... This may take some time.')
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(func) for func in functions]
        for future in as_completed(futures):
            try:
                result = future.result()
                results.extend(result)
            except Exception as e:
                print(f"An error occurred: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Providing {len(results)} releases to {request_from} for {stype}. Time taken: {elapsed_time:.2f} seconds")

    return results

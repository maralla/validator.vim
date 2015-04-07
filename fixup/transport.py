# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import select
import socket
import SocketServer
import struct

from .utils import logging


def recv_all(sock):
    length = sock.recv(4)
    if not length:
        return -1

    size = struct.unpack("!i", length)[0]

    data = sock.recv(size)
    while len(data) < size:
        data += sock.recv(size - len(data))

    return data


class ServerHandler(SocketServer.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server

        self.response = {}

    def reply(self):
        logging.debug("reply data {}".format(self.response))
        data = json.dumps(self.response)
        length = struct.pack("!i", len(data))
        self.request.sendall(length + data)
        logging.error("hello reply {}".format(self.response))

    def check(self, req):
        return "undefined"

    def handle(self):
        logging.info("handle")

        self.response = {"reply": []}

        req = recv_all(self.request)
        if req == -1:
            return req

        logging.info("req {}".format(req))
        req = json.loads(req)

        if req["cmd"] == "exit":
            self.response["reply"] = "exit"
        elif req["cmd"] == "ping":
            self.response["reply"] = "pong"
        elif req["cmd"] == "check":
            r = self.check(req)
            self.response["reply"] = r
            self.response["bufnr"] = req["bufnr"]

        logging.info("end handle")
        return 0


class FuServer(SocketServer.TCPServer):
    def __init__(self, *args, **kwargs):
        SocketServer.TCPServer.__init__(self, *args, **kwargs)
        self.client_map = {}

    def serve_forever(self):
        reads = [self.socket]
        writes = []

        while True:
            rs, ws, _ = select.select(reads, writes, [])
            for r in rs:
                if r is self.socket:
                    req, addr = self.socket.accept()
                    self.client_map[req] = self.RequestHandlerClass(
                        req, addr, self)
                    reads.append(req)
                else:
                    status = self.client_map[r].handle()
                    reads.remove(r)

                    if status != -1:
                        writes.append(r)

            for w in ws:
                if w not in self.client_map:
                    continue

                self.client_map[w].reply()
                writes.remove(w)
                reads.append(w)


class FuClient(object):
    def __init__(self, port, bulk_size=4096):
        self.port = port
        self.bulk_size = bulk_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_started = False

    def connect(self):
        self.sock.connect(("localhost", self.port))

    def send(self, data):
        data = json.dumps(data)
        length = struct.pack("!i", len(data))
        self.sock.send(length + data)

    def recv(self):
        data = recv_all(self.sock)

        try:
            res = json.loads(data)
        except:
            res = {"reply": {}}
        return res

    def close(self):
        self.sock.close()


def make_server(port, handler_class=ServerHandler):
    server = FuServer(("localhost", port), handler_class)
    return server


def event_loop(client, queue, job_func=None):
    while True:
        task = queue.get()
        if not client.server_started:
            if task["cmd"] == "exit":
                break

            continue

        logging.info("send task {}".format(task))
        client.send(task)
        res = client.recv()

        if res["reply"] == "exit":
            break

        if job_func:
            job_func(res)

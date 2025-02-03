import dns.resolver
import httpx
from typing import Optional, Any, Dict


class ServiceClient:
    def __init__(self, srv_record: str):
        """
        Initialize with the given SRV record.
        
        :param srv_record: The DNS SRV record used for service discovery.
        """
        self.srv_record = srv_record
        self.last_index = -1

    def resolve_instances(self):
        """
        Resolve the SRV record and return a sorted list of (target, port) tuples.
        Sorting ensures that the order remains consistent across calls.
        
        :return: Sorted list of (target, port) tuples.
        """
        try:
            answers = dns.resolver.resolve(self.srv_record, "SRV")
        except Exception as e:
            raise RuntimeError(f"Failed to resolve SRV record '{self.srv_record}': {e}")

        instances = []
        for srv in answers:
            target = str(srv.target).rstrip(".")
            port = srv.port
            instances.append((target, port))
            # Optionally log or print discovered instances
            # print(f"Discovered instance: {target}:{port}")

        if not instances:
            raise RuntimeError(f"No instances found for SRV record '{self.srv_record}'")

        # Sort instances by target and port for a consistent order
        instances.sort(key=lambda x: (x[0], x[1]))
        return instances

    def get_next_instance(self):
        """
        Select the next instance in a round-robin fashion from the sorted instance list.
        
        :return: A tuple (target, port) for the next service instance.
        """
        instances = self.resolve_instances()
        self.last_index = (self.last_index + 1) % len(instances)
        return instances[self.last_index]

    def call(
        self,
        path: str,
        method: str = "GET",
        body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 1800,
    ):
        """
        Make an HTTP request to the service using the discovered instance.
        
        :param path: The endpoint path (e.g., "/team/health"). A leading "/" will be added if missing.
        :param method: HTTP method to use ("GET", "POST", "PUT", "DELETE", etc.).
        :param body: (Optional) Request body (used for methods like POST/PUT).
        :param headers: (Optional) Dictionary of HTTP headers.
        :param timeout: (Optional) HTTP request timeout in seconds.
        :return: httpx.Response object.
        """
        target, port = self.get_next_instance()

        # Ensure that the path begins with a '/'
        if not path.startswith("/"):
            path = "/" + path

        url = f"http://{target}:{port}{path}"
        try:
            method = method.upper()
            if method == "GET":
                response = httpx.get(url, headers=headers, timeout=timeout)
            elif method == "POST":
                response = httpx.post(url, json=body, headers=headers, timeout=timeout)
            elif method == "PUT":
                response = httpx.put(url, json=body, headers=headers, timeout=timeout)
            elif method == "DELETE":
                response = httpx.delete(url, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response

        except Exception as e:
            raise RuntimeError(f"Failed to call service at {url}: {e}")

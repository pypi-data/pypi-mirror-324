
import os
from typing import List
import redis
from dotenv import load_dotenv
import requests
load_dotenv()

class Data3Utils:
    '''
    Class to fetch environment variables for the user tools file
    Methods:
    fetch_env_variables: Fetch Single or all ("") tool env values from Redis
    '''
    def __init__(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST")
        print("REDIS_HOST", self.REDIS_HOST)
        self.redis_client = redis.from_url(self.REDIS_HOST)
        print("REDIS_CLIENT", self.redis_client)
        self.rag_backend_url = self.fetch_base_url()
        print("RAG_BACKEND_URL", self.rag_backend_url)

    def fetch_env_variables(self,docker_service_name: str, field_names: List[str] = []):
        """Fetch a value from Redis and handle errors."""
        try:
            base_url = f"{self.rag_backend_url}:7000/get-tools-env"
            params = {"docker_service_name": docker_service_name}

            # Add `env_vars` only if the list is not empty
            if field_names:
                params["env_vars"] = field_names

            # Perform the GET request
            get_envs = requests.get(base_url, params=params)
            get_envs.raise_for_status()  # Raise an exception for HTTP errors

            # Print the response JSON
            print("Get Env Vars Response:", get_envs.json())
            return get_envs.json()

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"


        
    def fetch_port_by_address(self, agent_address: str):
        """Fetch a value from Redis and handle errors."""
        try:
            if agent_address:
                value = self.redis_client.hget("docker-compose-mappings", agent_address)
                if value == None:
                    return ValueError(f"Field {agent_address} not found in docker mappings")
                return value.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"  
        
    def fetch_port_by_service_name(self, service_name: str):
        """Fetch a value from Redis and handle errors."""
        try:
            if service_name:
                value = self.redis_client.hget("docker-service-mappings", service_name)
                if value == None:
                    return ValueError(f"Field {service_name} not found in docker mappings")
                return value.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"
    
    def fetch_port(self, service_name: str):
        """Fetch a value from Redis and handle errors."""
        try:
            if service_name:
                value = self.redis_client.hget(f"{service_name}_ENVS", "HOST_PORT")
                if value == None:
                    return ValueError(f"Field {service_name} not found in docker mappings")
                return value.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"
    

    def fetch_base_url(self):
        """Fetch a value from Redis and handle errors."""
        try:
            return "http://host.docker.internal"
        except Exception as e:
            return f"Error: {e}" 

    def fetch_custom_category_list(self):
        """Fetch a value from Redis and handle errors."""
        try:
            base_url = f"{self.rag_backend_url}:7000/custom-list"
            get_custom_categories = requests.get(base_url)
            return get_custom_categories.get('response', [])
        except Exception as e:
            return f"Error: {e}"
    
    def fetch_user_email(self):
        """Fetch a value from Redis and handle errors."""
        try:
            user_email = self.redis_client.hget("model_config", "user_email").decode('utf-8')
            return user_email
        except Exception as e:
            return f"Error: {e}"   

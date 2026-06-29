# Contract signing simulator for cloud-style systems
import hashlib
import json
import time
import uuid
from datetime import datetime

class ContractRecord:
    def __init__(self, owner, partner, agreement):
        self.owner = owner
        self.partner = partner
        self.agreement = agreement
        self.id = str(uuid.uuid4())
        self.created_at = time.time()
        self.events = []

    def serialize(self):
        return json.dumps({
            "id": self.id,
            "owner": self.owner,
            "partner": self.partner,
            "agreement": self.agreement,
            "created_at": self.created_at
        }, sort_keys=True)

    def digest(self):
        return hashlib.sha256(self.serialize().encode()).hexdigest()

    def sign(self, secret):
        base = self.digest()
        return hashlib.sha256(f"{base}:{secret}".encode()).hexdigest()

    def verify(self, signature, secret):
        return self.sign(secret) == signature

    def add_event(self, label):
        self.events.append({
            "label": label,
            "time": datetime.utcnow().isoformat()
        })

def workflow():
    contract = ContractRecord("OrgAlpha", "OrgBeta", "Data residency agreement")
    contract.add_event("created")

    hash_value = contract.digest()
    signature = contract.sign("aws_secret_key")

    contract.add_event("signed")

    print("Contract ID:", contract.id)
    print("Hash:", hash_value)
    print("Signature:", signature)
    print("Valid:", contract.verify(signature, "aws_secret_key"))

    contract.add_event("verified")
    return contract

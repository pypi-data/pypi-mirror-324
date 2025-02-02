from dawshs_jff.v12.hashes import generate_hash
from dawshs_jff.v12.samples import sample_requests



def test_h1_hash():
    for name, sample_request in sample_requests.items():
        assert (
            generate_hash(
                sample_request["client_ip"],
                sample_request["request_time"],
            )
            == sample_request["h1"]
        )

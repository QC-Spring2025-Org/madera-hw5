from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='0c6387e82de0da30b3c63bb7d0794c2e03f98064ec71f2776004d5749abd7d71136525d7f72d53e5437454574201e7297a26defb3f2bce8ee54c958b290eeb45'
)
job = service.job('cz8v134b7tt0008fz1jg')
job_result = job.result()
print(job_result)

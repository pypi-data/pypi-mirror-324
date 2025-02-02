"""
Tests for the jobs table.
"""

from .testing import make_job, kubectl_response, assert_query


def test_job_status(test_home):
    kubectl_response("jobs", {
        "items": [
            make_job("job-01"),
            make_job("job-02", active_count=1),
            make_job("job-03", namespace="xyz", condition=("Failed", "False", None)),
            make_job("job-04", namespace="xyz", condition=("Failed", "True", None)),
            make_job("job-05", condition=("Failed", "True", "DeadlineExceeded")),
            make_job("job-06", condition=("Suspended", "True", None)),
            make_job("job-07", condition=("Complete", "True", None)),
            make_job("job-08", condition=("FailureTarget", "False", None)),
            make_job("job-09", condition=("SuccessCriteriaMet", "False", None)),
            make_job("job-10", suspend=True),
        ]
    })
    assert_query("SELECT name, uid, namespace, status FROM jobs ORDER BY 1", """
        name    uid         namespace    status
        job-01  uid-job-01  example      Unknown
        job-02  uid-job-02  example      Running
        job-03  uid-job-03  xyz          Unknown
        job-04  uid-job-04  xyz          Failed
        job-05  uid-job-05  example      DeadlineExceeded
        job-06  uid-job-06  example      Suspended
        job-07  uid-job-07  example      Complete
        job-08  uid-job-08  example      Failed
        job-09  uid-job-09  example      Complete
        job-10  uid-job-10  example      Suspended
    """)


def test_job_labels(test_home):
    kubectl_response("jobs", {
        "items": [
            make_job("job-1", labels=dict(foo="bar")),
            make_job("job-2", labels=dict(a="b", c="d", e="f")),
            make_job("job-3", labels=dict()),
            make_job("job-4", labels=dict(one="two", three="four")),
        ]
    })
    assert_query("SELECT job_uid, key, value FROM job_labels ORDER BY 2, 1", """
        job_uid    key    value
        uid-job-2  a      b
        uid-job-2  c      d
        uid-job-2  e      f
        uid-job-1  foo    bar
        uid-job-4  one    two
        uid-job-4  three  four
    """)

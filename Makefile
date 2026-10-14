# Convenience targets. Every command also works typed out by hand.
PY ?= python3

.PHONY: test demo init doctor scan

test:            ## run the test suite (uses only the fictional demo workspace)
	$(PY) -m unittest discover -s tests

init:            ## create your personal workspace from the templates
	$(PY) scripts/init_workspace.py

doctor:          ## validate your workspace
	$(PY) scripts/doctor.py

demo:            ## run the pipeline on the FICTIONAL demo persona
	JOBSEARCH_WORKSPACE=examples/demo_persona/workspace $(PY) scripts/doctor.py
	JOBSEARCH_WORKSPACE=examples/demo_persona/workspace $(PY) scripts/resume_generator.py --spec resume_versions/2026-01-06_demo.json --dry-run
	JOBSEARCH_WORKSPACE=examples/demo_persona/workspace $(PY) scripts/check_company.py "Harbor Example Systems" --as-of 2026-01-05; test $$? -eq 1
	JOBSEARCH_WORKSPACE=examples/demo_persona/workspace $(PY) scripts/answer_check.py examples/demo_persona/workspace/cover_letters/2026-01-06_demo/screening_answers.md; test $$? -eq 1
	JOBSEARCH_WORKSPACE=examples/demo_persona/workspace $(PY) scripts/tracker_report.py --as-of 2026-01-15

scan:            ## release hygiene: scan the repo for personal data (add DENYLIST=path to use your own term list)
	$(PY) scripts/pii_scan.py --root . $(if $(DENYLIST),--denylist $(DENYLIST),)

.PHONY: prereqs check-ports pull cli up wait smoke pipeline demo assert stop clean all

prereqs:
	./scripts/00_install_ubuntu_prereqs.sh

check-ports:
	./scripts/01_check_ports.sh

pull:
	./scripts/02_pull_images.sh

cli:
	./scripts/03_download_trino_cli.sh

up:
	./scripts/04_start_stack.sh

wait:
	./scripts/05_wait_for_stack.sh

smoke:
	./scripts/06_smoke_trino.sh

pipeline:
	./scripts/07_run_pipeline.sh

demo:
	./scripts/08_demo_queries.sh

assert:
	./scripts/09_assert_expected_counts.sh

stop:
	./scripts/10_stop_stack.sh

clean:
	./scripts/11_clean_stack.sh

all: check-ports pull cli up wait smoke pipeline demo assert

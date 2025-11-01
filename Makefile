.PHONY: run demo

run:
	python app/game.py

demo:
	bash scripts/demo.sh | tee -a traces/run-log.txt

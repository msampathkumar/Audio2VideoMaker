
test_run: cleanup_test_run
	pip install -r requirements.txt --quiet && \
	python main.py ../data/sample_data/config.yaml test && \
	python main.py ../data/sample_data/config.yaml image && \
	python main.py ../data/sample_data/config.yaml video

cleanup_test_run:
	rm my_image.png && rm ../data/sample_data/*.mp4 && rm ../data/sample_data/*.png

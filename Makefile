SITE_PKG_PATH=`python3 -m site --user-site`

install:
	@rm -rf $(SITE_PKG_PATH)/gauss_keeker*
	python3 setup.py install --user --no-compile
	rm -r build

test: install
	python3 tests/test_all.py
	

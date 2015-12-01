==========================
EPFL Python Frontend Logic
==========================

To install:
-----------

	mkdir epfl; cd epfl
	virtualenv env
	source env/bin/activate
	pip install -e git+https://github.com/solute/pyramid_epfl.git#egg=pyramid_epfl
	pcreate -s pyramid_epfl_notes notes_app
	cd notes_app
	python setup.py develop
	pserve development.ini


Documentation:
--------------

Lives at http://pyramid-epfl.readthedocs.org/en/latest/


Notice:
-------

This software contains a Highsoft software product (Highcharts JS) that is not free for commercial use (http://www.highcharts.com/license).
For more information, visit http://www.highcharts.com/
  




# Copyright (c) 2015, Artech and Contributors
# See license.txt

import artech_engine
from artech_engine.utils import random_string

from artech.tests.utils import ArtechTestSuite


class TestVehicle(ArtechTestSuite):
	def test_make_vehicle(self):
		vehicle = artech_engine.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": artech_engine.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": artech_engine.utils.flt(500000),
			}
		)
		vehicle.insert()

	def test_renaming_vehicle(self):
		license_plate = random_string(10).upper()

		vehicle = artech_engine.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": license_plate,
				"make": "Skoda",
				"model": "Slavia",
				"last_odometer": 5000,
				"acquisition_date": artech_engine.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234EFGH",
				"uom": "Litre",
				"vehicle_value": artech_engine.utils.flt(500000),
			}
		)
		vehicle.insert()

		new_license_plate = random_string(10).upper()
		artech_engine.rename_doc("Vehicle", license_plate, new_license_plate)

		self.assertEqual(
			new_license_plate, artech_engine.db.get_value("Vehicle", new_license_plate, "license_plate")
		)

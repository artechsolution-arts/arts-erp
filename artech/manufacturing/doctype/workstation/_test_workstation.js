// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Workstation", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	artech_engine.run_serially("Workstation", [
		// insert a new Workstation
		() =>
			artech_engine.tests.make([
				// values to be set
				{ key: "value" },
			]),
		() => {
			assert.equal(cur_frm.doc.key, "value");
		},
		() => done(),
	]);
});

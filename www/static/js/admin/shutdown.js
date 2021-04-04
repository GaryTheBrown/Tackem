(function () {
	$(() => {
		$.ajax({
			type: 'GET',
			url: '/api/admin/shutdown/',
			success: function (json) {
				if (json.success) {
					$("h1").append("Done");
				} else {
					$("h1").append("Failed");
				}
			}
		})
	})
})();

(function () {
	$(() => {
		$.ajax({
			type: 'GET',
			url: '/api/admin/reboot/',
			success: function (json) {
				if (json.success) {
					$("h1").append("Done");
					$("h2").removeAttr('hidden');
					window.setTimeout(function () {
						window.location.href = '{{ baseurl }}';
						return false;
					}, 10000);
				} else {
					$("h1").append("Failed");
				}
			}
		})
	})
})();

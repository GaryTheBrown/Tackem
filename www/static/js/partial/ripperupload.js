(function () {

    $(() => {
        new RipperUpload();
    });

    class RipperUpload
    {
        constructor()
        {
            $('.custom-file-upload input[type="file"]').each(function () {
                $(this).bind('change', function () {
                    let file = this.files[0];
                    if (confirm(`upload ${file.name}`)) {
                        ShowLoader("UPLOADING");
                        $.ajax({
                            type: 'POST',
                            url: $(this).data("url"),
                            data: {
                                filename: file.name,
                                filesize: file.size
                            },
                            dataType: 'json',
                            success: function (result) {
                                fetch(ROOT + result.url, {method:"POST", body:file})
                                .then(response => {
                                    if (response.ok) {
                                        return response;
                                    } else {
                                        throw Error(`Server returned ${response.status}: ${response.statusText}`);
                                    }
                                })
                                .then(response => {
                                    HideLoader();
                                    $(this).val('');
                                })
                                .catch(err => {
                                    alert(err);
                                    $(this).val('');
                                });
                            },
                        });
                    } else {
                        $(this).val('');
                    }
                });
            });
        }
    }

})();

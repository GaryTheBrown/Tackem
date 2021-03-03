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
                        //TODO show uploading popup blocking the rest of the window
                        $.ajax({
                            type: 'POST',
                            url: $(this).data("url"),
                            data: {
                                filename: file.name,
                                filesize: file.size
                            },
                            dataType: 'json',
                            success: function (result) {
                                fetch(result.url, {method:"POST", body:file})
                                .then(response => {
                                    if (response.ok) {
                                        alert("File Uploaded");
                                        return response;
                                    } else {
                                        throw Error(`Server returned ${response.status}: ${response.statusText}`);
                                    }
                                })
                                .then(response => {
                                    //TODO return control back to screen
                                })
                                .catch(err => {
                                    alert(err);
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

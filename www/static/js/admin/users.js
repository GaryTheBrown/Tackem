(function () {

    $(() => {
        new Users();
    });

    class Users
    {
        constructor()
        {
            $("[data-action='delete']").on("click", this.delete);
            $("[data-action='update']").on("click", this.update);
            $("[data-action='add']").on("click", this.add);
        }

        delete()
        {
            let $elem = $(this);
            let $section = $elem.closest("section");
            let userid = $section.data("id");
            let username = $section.find("[name='username']").val();

            $elem.prop('disabled', true);

            if (confirm("Do you really want to Delete " + username + "?")){
                $.ajax({
                    type: 'DELETE',
                    url: ROOT + 'api/admin/userDelete/' + userid,
                    success: function(json)
                    {
                        if (json.success){
                            $section.remove();
                        } else {
                            if(json.message){
                                alert(message);
                            }

                        }
                    }
                });
            }else {
                $elem.prop('disabled', false);
            }
        }

        update()
        {
            let $elem = $(this);
            let $section = $elem.closest("section");
            let userid = $section.data("id");
            let username = $section.find("[name='username']").val();
            let password = $section.find("[name='password']").val();
            let isadmin = $section.find("[name='isadmin']").prop("checked");
            $elem.prop('disabled', true);

            $.ajax({
                type: 'POST',
                url: ROOT + 'api/admin/userUpdate/' + userid,
                data: {
                    username: username,
                    password: password,
                    isadmin: isadmin,
                },
                success: function(json)
                {
                    if (json.success){
                        $elem.prop('disabled', false);
                    } else {
                        if(json.message){
                            alert(message);
                        }
                    }
                }
            });
        }

        add()
        {
            let $elem = $(this);
            let $section = $elem.closest("section");
            let username = $section.find("[name='username']").val();
            let password = $section.find("[name='password']").val();
            let isadmin = $section.find("[name='isadmin']").prop("checked");

            $elem.prop('disabled', true);

            $.ajax({
                type: 'POST',
                url: ROOT + 'api/admin/userAdd/',
                data: {
                    username: username,
                    password: password,
                    isadmin: isadmin,
                },
                success: function(json)
                {
                    if (json.success){
                        location.reload();
                    } else {
                        if(json.message){
                            alert(message);
                        }
                    }
                }
            });
        }
    }

})();

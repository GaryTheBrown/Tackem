function GenerateAPIKey(input){
    num = Math.random().toString(36).substring(2, 12);
    num += Math.random().toString(36).substring(2, 12);
    num += Math.random().toString(36).substring(2, 12);
    num += Math.random().toString(36).substring(2, 12);
    $('#' + input).val(num);
}

function DeleteSection(plugin, name) {
    var confirmMessage = "Are you sure you want to delete " + name;
    if (confirm(confirmMessage)) {
        $("#" + plugin + "_" + name + "_delete_section").remove();
        if ($('#' + plugin + '_modal #' + plugin + '_name').is("select")){
            $('#' + plugin + '_modal select option[value="' + name + '"]').show();
        }
    }
}

function EnableDisable(section, disable, set){
    if (disable){
        $('#' + section + '_enabled').bootstrapToggle('on');
        $('#' + section + '_enabled').bootstrapToggle('disable');
    }else{
        $('#' + section + '_enabled').bootstrapToggle('enable');
    }
    if (set != null){
        $('#' + section + '_enabled').prop('checked', set);
    }
}
function Switch(section){
    if($('#'+ section).is(':checked')){
        $('#h_'+ section).val("True");
    }else{
        $('#h_'+ section).val("False");
    }
}

function ToggleSection(section){
    if($('#'+ section + '_enabled').is(':checked')){
        $('#'+ section + '_section').show();
    }else{
        $('#'+ section + '_section').hide();
    }
}

function ToggleSections(show, hide){
    for (var showSection in show) {
        $('#'+ show[showSection] + '_section').show();
    }
    for (var hideSection in hide) {
        $('#'+ hide[hideSection] + '_section').hide();
    }
}


function contains(array, needle) {
    for (var i in array) {
        if (array[i] == needle) return true;
    }
    return false;
}

function AddMulti(plugin){
    var save_list = Array();
    $("#" + plugin + "_section > div").each(function( index ) {
        save_list.push($( this ).attr( "id" ));
    });
    var name = $('#' + plugin + '_modal').find('#' + plugin + '_name').val();
    name = name.replace(/\s/g, '');
    if (name != "" && name != null) {
        var save_name = plugin + "_" + name + "_delete_section";
        if(contains(save_list, save_name)){
            $('#' + plugin + '_modal').find('#' + plugin + '_name').val('');
            $('#' + plugin + "_name_empty" ).hide();
            $('#' + plugin + "_name_duplicate").show();
        }else{
            $('#' + plugin + "_name_empty" ).hide();
            $('#' + plugin + "_name_duplicate").hide();
            $.get("/get_multi_setup?plugin=" + plugin + "&name=" + name, function (data) {
                save_list.push(save_name);
                $('#' + plugin + "_section").append(data);
                $('#' + plugin + "_section").show();
                $('#' + plugin + '_modal').modal('hide');
                $('#' + plugin + '_modal').find('#' + plugin + '_name').val("");
                if ($('#' + plugin + '_modal #' + plugin + '_name').is("select")){
                    $('#' + plugin + '_modal select option[value="' + name + '"]').hide();
                }
                $('#' + plugin + '_' + name + '_enabled').bootstrapToggle();
                var mylist = $('#' + plugin + "_section");
                var listitems = mylist.children('div').get();
                listitems.sort(function (a, b) {
                    var compA = $(a).attr('id').toUpperCase();
                    var compB = $(b).attr('id').toUpperCase();
                    return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
                });
                $.each(listitems, function (idx, itm) {
                    mylist.append(itm);
                });
            });
        }
    }else{
        $('#' + plugin + "_name_empty" ).show();
        $('#' + plugin + "_name_duplicate").hide();
    }
    return true;
}

var pluginList = []

function DownloadPlugin(pluginName, full_system){
    $('#dim_screen').show();
    input = $("#" + pluginName + "_control");
    $("#" + pluginName + "_control > input").prop('disabled', true);
    $.ajax({
        type: 'GET',
        url: '/download_plugin?name=' + pluginName,
        input: input,
        pluginName: pluginName,
        success: function(data) {
            this.input.html(data);
            alert(this.pluginName + " Downloaded");
            count = parseInt($("#plugin_count").val());
            count++;
            $("#plugin_count").val(count);
            newCount = parseInt($("#new_plugin_count").val());
            if (pluginList.includes(this.pluginName)){
                newCount--;
                pluginList = pluginList.filter(e => e !== this.pluginName);
            }else{
                newCount++;
                pluginList.push(this.pluginName);
            }
            $("#new_plugin_count").val(newCount);
            if (newCount == 0){
                $('input[value="Restart"]').hide();
                $("button").prop("disabled", true);
            }else{
                $('input[value="Restart"]').show();
                $("button").prop("disabled", true);
            }
            $('#dim_screen').hide();
        }
   });
}

function RemovePlugin(pluginName){
    $('#dim_screen').show();
    input = $("#" + pluginName + "_control");
    $("#" + pluginName + "_control > input").prop('disabled', true);
    $.ajax({
        type: 'GET',
        url: '/remove_plugin?name=' + pluginName,
        input: input,
        pluginName: pluginName,
        success: function(data) {
            this.input.html(data);
            alert(this.pluginName + " Removed");
            count = parseInt($("#plugin_count").val());
            count--;
            $("#plugin_count").val(count);
            newCount = parseInt($("#new_plugin_count").val());
            if (pluginList.includes(this.pluginName)){
                newCount--;
                pluginList = pluginList.filter(e => e !== this.pluginName);
            }else{
                newCount++;
                pluginList.push(this.pluginName);
            }
            $("#new_plugin_count").val(newCount);
            if (newCount == 0){
                $('input[value="Restart"]').hide();
                $("button").prop("disabled", true);
            }else{
                $('input[value="Restart"]').show();
                $("button").prop("disabled", true);
            }
            $('#dim_screen').hide();
        }
   });
}

function CheckLive () {
    $.ajax({
        url: "/is_live",
        type: "GET",
        success: function () {
            clearTimeout(CheckLive);
            $("#page_index").val(2);
            $("form").submit();
        },
        error: function () {
            setTimeout(() => {
                CheckLive()
            }, 5000)
        }
    })
  }

function Restart(){
    $('#dim_screen').show();
    $('input[value="Restart"]').hide();
    $.ajax({
        type: 'GET',
        url: '/restart',
        success: function(data) {
            setTimeout(function(){CheckLive();}, 10000);
            
        }
   });
}
function ShowLoader(message = "LOADING")
{
    $("#loading-popup").show();
    $("#loading-popup").find("h1").html(message);
}

function HideLoader()
{
    $("#loading-popup").hide();
    $("#loading-popup").find("h1").html("");
}

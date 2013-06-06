function showdetails(id, url)
{
    var xmlhttp;
    var x, i;
    if (window.XMLHttpRequest)
    {
        xmlhttp=new XMLHttpRequest();
    }
    else
    {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    // hide other detail info before open specified one
    x = document.getElementsByTagName("div");
    for (i = 0; i < x.length; i++)
    {
        x[i].innerHTML = "";
    }
    //
    xmlhttp.onreadystatechange=function()
    {
        if ( xmlhttp.readyState==4 )
        {
            if ( xmlhttp.status==200 )
            {
                document.getElementById(id).innerHTML = xmlhttp.responseText+"<center><button onclick=hidethis("+id+")>hide this</button></center>";
            }
            else
            {
                document.getElementById(id).innerHTML = "<center>Error occur!</center>"
            }
        }
        else
        {
            document.getElementById(id).innerHTML = "<center>processing...</center>"
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}

function hidethis(id)
{
    document.getElementById(id).innerHTML = "";
}

function gethn()
{
    $("td.name").each(function(){
        var host = $(this).attr("id");
        $(this).load("gh/"+host, function(responseTxt,statusTxt,xhr){
            if (xhr.readyState == 4 && xhr.status == 200)
            {
                if (responseTxt == "Not Available")
                {
                    $(this).next().replaceWith("<button disabled='disabled'>details</button>");
                }
            }
        })
    })
}

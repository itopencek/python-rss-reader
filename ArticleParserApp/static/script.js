$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});

function addSite(name, url, desc, lang) {
    console.log(lang)
    $.ajax({
        type: 'POST',
        url: '/api/site',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ name: name, url: url, description: desc, language: lang }),
        success: function (data) {
            console.log("Successfully added site")
            location.reload()
        }
    });
}

function createRequest(url, type) {
    $.ajax({
        type: type,
        url: url,
        success: function (data) {
            console.log("Successfull request")
            location.reload()
        }
    });
}

function epochToDate() {
    console.log("test")
    return "123"
}
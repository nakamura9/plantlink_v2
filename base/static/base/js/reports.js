$(document).ready(function(){
    if($('form').find('input[type="submit"]').length == 0) {
        $('form').append(`<input type="submit" name="submit" value="Render" class="btn btn-primary"/>`)
    }
    $('form').on('submit', evt =>{
        evt.preventDefault()
        const url_parts = location.href.split('/')
        const name = url_parts[url_parts.length -2]
        const path = '/get-report-data/' + name  +'/'
        $('#form_data').val($('form').serialize())
        $.ajax({
            url: path,
            method: 'POST',
            data: $('form').serialize()
        }).then(function(data) {
            $('#report-body').html(data)
        }).catch(err => {
            console.log(err)
            alert("An error occurred rendering this report.")
        })
    })

    $("#pdf").on("click", function() {
        console.log("clicked")
        const url_parts = location.href.split('/')
        const report_name = url_parts[url_parts.length - 2]
        window.location.href = '/report-pdf/' + report_name + '/?' + $('form').serialize()
    })
})


$(document).ready(function(){
    $("#image_file").on("change", function() {
      var fileName = $(this).val().split("\\").pop();
      $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    $("#image_upload_image_button").click(function(){
        $("#image_upload_modal").modal();
    });

    $('#upload_image_button').click(function(){
        var form_data = new FormData($('#image_upload_form')[0]);
        if ($("#image_for_select").val() != '0'){
            $.ajax({
                type:'post',
                url:$SCRIPT_ROOT + '/_upload_image',
                data: form_data,
                dataType:'json',
                contentType: false,
                cache: false,
                processData:false,
                success:function(response){
                    if (response.status == "OK"){
                        location.reload();
                    }else if (response.status == "ERROR"){
                        location.reload();
                    }
                },
                error:function(response){
                  console.log("Error ! Try again after a while.");
                }
          });
        }
    });
});
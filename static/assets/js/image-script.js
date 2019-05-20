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

    $(".delete_image").click(function(){
        var image_name = $(this).children(".image_name").val();
        var image_id = $(this).children(".image_id").val();
        $("#image_id").val(image_id);
        $("#image_name").val(image_name);
        $("#delete_image_warning_modal").modal();
    });

     $(".view_image").click(function(){
        $("#image_display").modal();
        var source_root = $(this).attr('src');
        $("#max-image").attr("src",".."+source_root);
    });

    $("#confirm_delete").click(function(){
        var image_id = $('#image_id').val();
        var image_name = $('#image_name').val();

        $.ajax({
                type:'post',
                url:$SCRIPT_ROOT + '/_delete_image',
                data:{
                    image_name:image_name,
                    image_id:image_id
                },
                dataType:'json',
                success:function(response){
                    if (response.status == "OK"){
                        location.reload();
                    }else{
                        location.reload();
                    }
                },
                error:function(response){
                  console.log("Error ! Try again after a while.");
                }
          });
    });
});
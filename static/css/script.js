$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-body input').val(recipient)
})

$('#inputGroupFile01').on('change',function(){
  //get the file name
  var fileName = $(this).val().replace('C:\\fakepath\\', " ");
  //replace the "Choose a file" label
  $(this).next('.custom-file-label').html(fileName);
})
// Material Select Initialization
$(document).ready(function() {
$('.mdb-select').materialSelect();
});
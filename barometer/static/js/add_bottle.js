$(function() {
	$('[name=description]').focus();
	$('#new_category').hide();
	$('#new_subcategory').hide();
	update_subtypes();
	$('#category').bind('change', update_subtypes);
	$('#subcategory').bind('change', function() {
		val = $('#subcategory').val();
		if(val == 'new') {
			$('#new_subcategory').show().focus();
		} else {
			$('#new_subcategory').hide();
		}
	});
});

function update_subtypes() {
	val = $('#category').val();
	$('#new_subcategory').hide();
	$('#subcategory').val('');
	$('#subcategory option.contextual').hide();
	if(val == 'new') {
		$('#new_category').show().focus();
		$('#subcategory option.contextual').hide();
	} else {
		$('#new_category').hide();
		$('#subcategory option.'+val).show();
	}
}

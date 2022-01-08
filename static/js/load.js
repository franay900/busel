



jQuery(document).ready(function(){
$('.timetable').click(function(){
	let td=$(this).parent('td')
	
	$('#begin').clone().appendTo(td).css('display','block').attr('name','begin_'+$(this).val())
	$('#end').clone().appendTo(td).css('display','block').attr('name','end_'+$(this).val())
	$(this).css('display','none')
})


$('.delete').click(function(){
	$('#exampleModal').modal('show')
	$('.cancel').attr('element',$(this).attr('id'))
	})

$('.cancel').click(function(){
	var element=$(this).attr('element')
	$('#'+element).prop('checked',false)



	})

$('.confirm').click(function(){

	$('#exampleModal').modal('toggle')


})


});
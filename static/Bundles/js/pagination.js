function clear_form(form){
	form.trigger("reset");
	form.find(".select2_input").each(function(){
		$(this).val("-1").trigger("change");
	});
	form.find(".password").each(function(){
		$(this).prop('required',true);
		$(this).removeAttr("disabled");
	});
	form.find("[name=pk]").each(function(){
		$(this).removeAttr("value");
	});
	$("#"+form.attr("id")+"_error").parent().hide()
	$("#"+form.attr("id")+"_error").html("")
}
$(document).ready(function() {
	$("#second_page").css("display","none");
	$("#first").parent().addClass("active");
	if(document.getElementsByClassName("pagination_container")[0]) {
		$('#first').click(function() {
			$(this).parent().addClass("active");
			$("#second").parent().removeClass("active");
			$("#third").parent().removeClass("active");

			$("#first_page").css("display","block");
			$("#second_page").css("display","none");
			$("#third_page").css("display","none"); 
		})

		$('#second').click(function() {
			$(this).parent().addClass("active");
			$("#first").parent().removeClass("active");
			$("#third").parent().removeClass("active");

			$("#first_page").css("display","none");
			$("#second_page").css("display","block");
			$("#third_page").css("display","none");
		})

		$('#third').click(function() {
			$(this).parent().addClass("active");
			$("#second").parent().removeClass("active");
			$("#first").parent().removeClass("active");

			$("#first_page").css("display","none");
			$("#second_page").css("display","none");
			$("#third_page").css("display","block");
		})
	}
})

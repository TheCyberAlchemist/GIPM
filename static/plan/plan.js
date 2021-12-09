$(function() {

	clear_form($(".myform"))

	demo2 = $('.multiselect').bootstrapDualListbox({
		nonSelectedListLabel: 'Non-selected',
		selectedListLabel: 'Selected',
		preserveSelectionOnMove:false,
		moveOnSelect: false,
		nonSelectedFilter: ''
	});

	$("#refresh_list").on("click",function(){
		$(".spinner-border").show();
		refresh_options();
	})

	$("#save_plan").on("click",function(){
		save_plan();
	})
	$("#update_plan").on("click",function(){
		update_plan();
	})
	

	// for (i of demo2.val()){
	// 	add_to_mirror($("option[value='"+i+"']").first());
	// }
	$("tr input").on('keyup',function(e){
		calculate_total();
	})
	$("tr input").on("change",function(){
		calculate_total();
	})
});

function delete_options(options){
	options.each(function(index, option) {
		var $option = $(option);
		let pk = $option.val();
		console.log($("[value='"+pk+"']"),pk)
		$("[value='"+pk+"']").remove();

	})
}

function refresh_options(){
	$.ajax({
		url: '/api/assembly',
		type: "get",
		success: function (all_assemblies) {
			delete_options(demo2.bootstrapDualListbox('getDeselected'));
			demo2.bootstrapDualListbox('refresh');
			let selected_options = demo2.bootstrapDualListbox('getSelected');
			for(assembly of all_assemblies){
				let option_selected = false;
				selected_options.each(function (index, option) {
					if (option.value == assembly.id){
						option_selected = true;
					}
				})
				if (!option_selected){
					let option = `<option value="${assembly.id}" data-ev = "${assembly.estimate_value}">${assembly.name}</option>`;
					demo2.append(option);
					demo2.bootstrapDualListbox('refresh');
				}
			}
			$(".spinner-border").hide();
		},
		error: function (response) {
			$(".spinner-border").hide();
		}
	})
}
// #region add and remove from mirror
function add_to_mirror(options){
	options.each(function(index, option) {
		var $option = $(option);
		let option_str = 
		`
			<tr data-ev="${$option.data('ev')}" data-pk="${$option.val()}" id="tr_item_${$option.val()}">
				<td>${$option.html()}</td>
				<td>${$option.data('ev')}</td>
				<td><input type='number' value='1' class = "quantity_input" id='quantity_${$option.val()}' min='0'></td>
			</tr>
		`;
		$("#mirror").append(option_str)
		$(`#tr_item_${$option.val()} input`).on('keyup',function(e){
			calculate_total();
		})
		$(`#tr_item_${$option.val()} input`).on("change",function(){
			calculate_total();
		})
	})
	calculate_total()
}

function remove_from_mirror(options){
	options.each(function(index, option) {
		var $option = $(option);
		$("#mirror").find(`[data-pk=${$option.val()}]`).remove();
	})
	calculate_total();
}
// #endregion

// #region move-remove functions
function optionMoved(obj){
	add_to_mirror(obj);
	// console.log("optionMoved",obj);
}

function optionRemoved(obj){
	remove_from_mirror(obj)
	// console.log("optionRemoved",obj);
}

function allOptionMoved(obj){
	add_to_mirror(obj);
	// console.log("allOptionMoved",obj);
}

function allOptionRemoved(obj){
	remove_from_mirror(obj)
	// console.log("allOptionRemoved",obj);
}
// #endregion

function get_assembly_and_json(){
	let assembly_json = {};
	let assemblies = [];
	$("#mirror tr").each(function(i,tr){
		tr = $(tr);
		let pk = tr.data("pk");
		let quantity = tr.find(".quantity_input").val();
		assemblies.push(pk);
		assembly_json[pk] = {
			"quantity": quantity || 0,
		};
	})
	return [assembly_json,assemblies]
}

function calculate_total(){
	let total = 0;
	let [assembly_json,assemblies] = get_assembly_and_json();
	$.ajax({
		url: '/api/plan/calculate-estimate',
		data : {"assembly_json": JSON.stringify(assembly_json)},
		dataType: 'json',
		success: function (response) {
			console.log(response);
			total = response;
			if (!total){
				total = 0.00;
			}
			$("#total_estimate").html(total);
		},
		error: function (response) {
			console.log(response);
		}
	})

}

function update_plan(){
	let form = $(".myform");
	let estimate_value = parseFloat($("#total_estimate").html());
	let [assembly_json,assemblies] = get_assembly_and_json();
	let form_data = {
		"name": $("#name").val(),
		"description": $("#description").val(),
		"assembly_json":JSON.stringify(assembly_json),
		"assemblies": assemblies,
		"estimate_value":estimate_value,
	}
	let form_method = "PUT";
	let form_url = `/api/plan/${plan_id}/`;
	// console.log(form_data)
	$.ajax({
		url: form_url,
		data : JSON.stringify(form_data),
		type: form_method,
		contentType: "application/json; charset=utf-8",
		success: function (response) {
			console.log(response);
			if (response.success){
				$("#mirror").html("");
				clear_form(form)
			}
		},
		error: function (response) {
			console.log(response);
		}
	})
}

function save_plan(){
	let form = $(".myform");
	let [assembly_json,assemblies] = get_assembly_and_json();
	let form_data = {
		"name": $("#name").val(),
		"description": $("#description").val(),
		"assembly_json":JSON.stringify(assembly_json),
		"assemblies": assemblies,
	}
	let form_method = "POST";
	let form_url = "/api/plan";
	console.log(form_data)
	$.ajax({
		url: form_url,
		data : JSON.stringify(form_data),
		type: form_method,
		contentType: "application/json; charset=utf-8",
		success: function (response) {
			console.log(response);
			alert("Plan saved successfully");
		},
		error: function (response) {
			console.log(response);
		}
	})
}
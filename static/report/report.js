function convertNumberToWords(amount) {
    var words = new Array();
    words[0] = '';
    words[1] = 'One';
    words[2] = 'Two';
    words[3] = 'Three';
    words[4] = 'Four';
    words[5] = 'Five';
    words[6] = 'Six';
    words[7] = 'Seven';
    words[8] = 'Eight';
    words[9] = 'Nine';
    words[10] = 'Ten';
    words[11] = 'Eleven';
    words[12] = 'Twelve';
    words[13] = 'Thirteen';
    words[14] = 'Fourteen';
    words[15] = 'Fifteen';
    words[16] = 'Sixteen';
    words[17] = 'Seventeen';
    words[18] = 'Eighteen';
    words[19] = 'Nineteen';
    words[20] = 'Twenty';
    words[30] = 'Thirty';
    words[40] = 'Forty';
    words[50] = 'Fifty';
    words[60] = 'Sixty';
    words[70] = 'Seventy';
    words[80] = 'Eighty';
    words[90] = 'Ninety';
    amount = amount.toString();
    var atemp = amount.split(".");
    var number = atemp[0].split(",").join("");
    var n_length = number.length;
    var words_string = "";
    if (n_length <= 9) {
        var n_array = new Array(0, 0, 0, 0, 0, 0, 0, 0, 0);
        var received_n_array = new Array();
        for (var i = 0; i < n_length; i++) {
            received_n_array[i] = number.substr(i, 1);
        }
        for (var i = 9 - n_length, j = 0; i < 9; i++, j++) {
            n_array[i] = received_n_array[j];
        }
        for (var i = 0, j = 1; i < 9; i++, j++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                if (n_array[i] == 1) {
                    n_array[j] = 10 + parseInt(n_array[j]);
                    n_array[i] = 0;
                }
            }
        }
        value = "";
        for (var i = 0; i < 9; i++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                value = n_array[i] * 10;
            } else {
                value = n_array[i];
            }
            if (value != 0) {
                words_string += words[value] + " ";
            }
            if ((i == 1 && value != 0) || (i == 0 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Crores ";
            }
            if ((i == 3 && value != 0) || (i == 2 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Lakhs ";
            }
            if ((i == 5 && value != 0) || (i == 4 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Thousand ";
            }
            if (i == 6 && value != 0 && (n_array[i + 1] != 0 && n_array[i + 2] != 0 && !atemp[1])) {
                words_string += "Hundred and ";
            } else if (i == 6 && value != 0) {
                words_string += "Hundred ";
            }
        }
        words_string = words_string.split("  ").join(" ");
    }
	words_string += "Rupees "
	if (atemp[1]){
		words_string += "and "
		let p_str = atemp[1];
        counter=0;
		for (i of p_str){
            if (counter == 0) {
                value = i * 10;
            } else {
                value = i;
            }
            if (value != 0) {
                words_string += words[value] + " ";
            }
            counter++;
		}
        if (p_str.length == 1){
        }
		words_string += "Paise"
	}
    return words_string;
}

function get_total_in_words(total) {
	let s = convertNumberToWords(total)
	document.getElementById("total_in_words").innerHTML += s
    change_currency();
}

function change_currency(){
    currency_td = document.querySelectorAll("td.currency");
    for (td of currency_td){
        input_val = td.innerHTML

        if (input_val === "") {
            return;
        }
    
        // original length
        var original_len = input_val.length;
    
        // initial caret position
        // check for decimal
        if (input_val.indexOf(".") >= 0) {
            // get position of first decimal
            // this prevents multiple decimals from
            // being entered
            var decimal_pos = input_val.indexOf(".");
    
            // split number by decimal point
            var left_side = input_val.substring(0, decimal_pos);
            var right_side = input_val.substring(decimal_pos);
    
            // add commas to left side of number
            left_side = formatNumber(left_side);
    
            // validate right side
            right_side = formatNumber(right_side);
    
            // On blur make sure 2 numbers after decimal
            if (blur === "blur") {
                right_side += "00";
            }
    
            // Limit decimal to only 2 digits
            right_side = right_side.substring(0, 2);
            if (right_side.length == 1){
                right_side+="0"
            }
            // join number by .
            input_val = "₹ " + left_side + "." + right_side;
        } else {
            // no decimal entered
            // add commas to number
            // remove all non-digits
            input_val = formatNumber(input_val);
            input_val = "₹ " + input_val;
    
            // final formatting
            if (blur === "blur") {
                input_val += ".00";
            }
        }
    
        // send updated string to input
        td.innerHTML = input_val
        
    }
}

function formatNumber(x) {
	x = x.replace(/\D/g, "")
	var lastThree = x.substring(x.length-3);
    var otherNumbers = x.substring(0,x.length-3);
    if(otherNumbers != ''){
        lastThree = ',' + lastThree;
	}
    var res = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;
	return res
}

function formatCurrency(input, blur) {
	// appends $ to value, validates decimal side
	// and puts cursor back in right position.

	// get input value
	var input_val = input.val();
	console.log(input_val)

	// don't validate empty input
	if (input_val === "") {
		return;
	}

	// original length
	var original_len = input_val.length;

	// initial caret position
	// check for decimal
	if (input_val.indexOf(".") >= 0) {
		// get position of first decimal
		// this prevents multiple decimals from
		// being entered
		var decimal_pos = input_val.indexOf(".");

		// split number by decimal point
		var left_side = input_val.substring(0, decimal_pos);
		var right_side = input_val.substring(decimal_pos);

		// add commas to left side of number
		left_side = formatNumber(left_side);

		// validate right side
		right_side = formatNumber(right_side);

		// On blur make sure 2 numbers after decimal
		if (blur === "blur") {
			right_side += "00";
		}

		// Limit decimal to only 2 digits
		right_side = right_side.substring(0, 2);
        if (right_side.length == 1){
            right_side+="0"
        }
		// join number by .
		input_val = "₹ " + left_side + "." + right_side;
	} else {
		// no decimal entered
		// add commas to number
		// remove all non-digits
		input_val = formatNumber(input_val);
		input_val = "₹ " + input_val;

		// final formatting
		if (blur === "blur") {
			input_val += ".00";
		}
	}

	// send updated string to input
    input.val(input_val)
}

if (typeof hotkeys !== 'undefined'){
    hotkeys("ctrl+q", function (event, handler) {
        switch (handler.key) {
            case "ctrl+q":
                $("#export_excel").click();
                break;
        }
    });
}

$(document).ready(function() {
    $("#lock_indent").click(function(){
        Swal.fire({
            icon: "question",
            title: 'Lock the indents?',
            input: 'text',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Lock',
            showLoaderOnConfirm: true,
            preConfirm: (password) => {
                if (password == "21149"){
                    return fetch(`./lock`)
                    .then(response => {
                        if (!response.ok) {
                        throw new Error(response.statusText)
                        }
                        return response.json()
                    })
                    .catch(error => {
                        Swal.showValidationMessage(
                        `Request failed: ${error}`
                        )
                    })
                }else{
                    swal.close()
                }
            },
            allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                console.log(result)
            if (result.value && result.value.done) {
                Swal.fire(
					'Indents Locked!',
                    "",
					'success'
				)
            }
        })
    })
    $("#lock_indent").click();

})

$(document).ready(function() {
			// To style all selects
		
	$('select').selectpicker();
		
			  
				
} );

$(document).ready(function() {
		var table = $('#mtgox').DataTable( {
			responsive: true,
			'searching'   : false,
			'paging'      : false,
			'ordering': false
			  
				
		} );
		 
	new $.fn.dataTable.FixedHeader( table );

} );

$(document).ready(function() {
		var table = $('#indicators').DataTable( {
			responsive: true,
			"pageLength": 50
				
					
		} );
		 
	new $.fn.dataTable.FixedHeader( table );
	// When the toggleNavbar button is clicked
	$("#toggleNavbar").click(function() {
		$(".vertical-navbar").toggle();  // Toggle the navbar visibility
		// Other code...

		// Recalculate the datatable dimensions after a slight delay
		setTimeout(function() {
			table.columns.adjust().responsive.recalc();
		}, 100);
	});

	// When the "Create table" button is clicked
	$(".cssbuttons-io-button").click(function() {
		$(".vertical-navbar").show();  // Show the navbar
		// Other code...

		// Recalculate the datatable dimensions after a slight delay
		setTimeout(function() {
			table.columns.adjust().responsive.recalc();
		}, 100);
	});

} );

$( "#hover" ).hover(function() {
	$( this ).fadeOut( 100 );
	$( this ).fadeIn( 500 );
});
		
$('#form_home_email').on('submit', function(e){
             
		e.preventDefault();
		var form = $("#form_home_email");
				
		$.ajax({
			type : "POST", 
			url: "/register_email",
			data: form.serialize(),								   
			success: function(data){
			Swal.fire({
			title: 'Success!',
			text: 'You email registered successfully',
			icon: 'success',
			})
			document.getElementById("inputemail").value = "";

		},
		error: function(XMLHttpRequest, textStatus, errorThrown) { 
                    //alert("Status: " + textStatus); alert("Error: " + errorThrown); 
			Swal.fire({
				title: 'Error!',
				text: 'Email can not registered',
				icon: 'error',
				})
			document.getElementById("inputemail").value = "";
        } 
				
	}); 
});

$('#form_home_email1').on('submit', function(e){
             
		e.preventDefault();
		var form = $("#form_home_email1");	
		$.ajax({
			type : "POST", 
			url: "/register_email",
			data: form.serialize(),								   
			success: function(data){					
				Swal.fire({
					title: 'Success!',
					text: 'You email registered successfully',
					icon: 'success',
				})
				document.getElementById("inputemail1").value = "";

			},
			error: function(XMLHttpRequest, textStatus, errorThrown) { 
						//alert("Status: " + textStatus); alert("Error: " + errorThrown); 
				Swal.fire({
					title: 'Error!',
					text: 'Email can not registered',
					icon: 'error',
					})
				document.getElementById("inputemail1").value = "";
			} 			
		}); 
}); 

		



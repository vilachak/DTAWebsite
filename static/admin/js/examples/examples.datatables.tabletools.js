/*
Name: 			Tables / Advanced - Examples
Written by: 	Okler Themes - (http://www.okler.net)
Theme Version: 	4.2.0
*/

(function($) {

	'use strict';

	var datatableInit = function() {
		var $table = $('#datatable-tabletools');

		var table = $table.dataTable({
			sDom: '<"text-right mb-md"T><"row"<"col-lg-6"l><"col-lg-6"f>><"table-responsive"t>p',
			buttons: [
				{
					extend: 'print',
					text: 'Print'
				},
				{
					extend: 'excel',
					text: 'Excel'
				},
				{
					extend: 'pdf',
					text: 'PDF',
					customize : function(doc){
			            var colCount = new Array();
			            $('#datatable-tabletools').find('tbody tr:first-child td').each(function(){
			                if($(this).attr('colspan')){
			                    for(var i=1;i<=$(this).attr('colspan');$i++){
			                        colCount.push('*');
			                    }
			                }else{ colCount.push('*'); }
			            });
			            doc.content[1].table.widths = colCount;
			        }
				}
			],
			
			drawCallback: function(){
				$('.paginate_button.next:not(.disabled)', this.api().table().container())          
				   .on('click', function(){
					  alert('next');
				   });       
			}
		});

		$('<div />').addClass('dt-buttons mb-2 pb-1 text-end').prependTo('#datatable-tabletools_wrapper');

		$table.DataTable().buttons().container().prependTo( '#datatable-tabletools_wrapper .dt-buttons' );

		$('#datatable-tabletools_wrapper').find('.btn-secondary').removeClass('btn-secondary').addClass('btn-default btn-sm');
	};

	$(function() {
		datatableInit();
	});

}).apply(this, [jQuery]);

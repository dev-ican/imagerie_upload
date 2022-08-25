$(document).ready(function() {
    var table = $('#tableau_etats').DataTable({
      paging: false,
      language: {
        url: '//cdn.datatables.net/plug-ins/1.12.1/i18n/fr-FR.json'
    },
      searchPanes: {
        layout: 'columns-5',
          viewTotal: true,
          orderable: false,
          controls: false
      },
      dom: 'Plfrtip',
      columnDefs: [
          {
              searchPanes: {
                  show: false
              },
              targets: [1, 2]
          }
      ]
  });

    table.columns().every( function() {
        var that = this;
  
        $('input', this.footer()).on('keyup change', function() {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
          }
      });
  });
});
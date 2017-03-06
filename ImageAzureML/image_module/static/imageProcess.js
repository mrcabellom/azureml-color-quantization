(function () {
    'use strict';

    var JOB_INTERVAL = 5000;
    var PROCESS_STATUS = 'Finished';
    var OUTPUT_PARAM = 'output_image';
    var $infoSection = $('.info-section');
    var $imagePreview = $('.image-preview');
    var $statusText = $('#statusText');

    function cleanSection() {
        $infoSection.addClass('hidden');
        $('.form-control').val('');
        $statusText.text('');
        $statusText.removeClass('label-success');
        $infoSection.find('.fa-spin').removeClass('hidden');
    }

    function getImage(blobResultData) {
        var datasetBlobInfo = blobResultData[OUTPUT_PARAM];
        var url = datasetBlobInfo.BaseLocation + datasetBlobInfo.RelativeLocation
        + datasetBlobInfo.SasBlobToken;
        ajaxCall(
           {
               url: '/image/filteredimage',
               method: 'POST',
               data: JSON.stringify({ 'blobUrl': url })
           },
           function (data) {
               $infoSection.filter('.result-image').removeClass('hidden');
               var filteredImage = document.getElementById('filteredImage');
               filteredImage.setAttribute('src', data.image_url);
           }, true);
    }

    function ajaxCall(params, callBack, isJsonContent) {
        var ajaxOptionsDefaultOptions = {
            success: callBack,
            processData: false
        };

        $.extend(ajaxOptionsDefaultOptions, params);
        ajaxOptionsDefaultOptions.contentType = isJsonContent
            ? 'application/json; charset=UTF-8' : false;
        $.ajax(ajaxOptionsDefaultOptions);
    }

    function getJobStatus(urlStatus) {
        $infoSection.filter('.status').removeClass('hidden');
        $statusText.text('Submitting Job')
        var interval = setInterval(function () {
            ajaxCall(
            {
                url: urlStatus,
                method: 'GET',
                dataType: "json"
            },
            function (data) {
                $statusText.text(data.StatusCode);
                if (data.StatusCode === PROCESS_STATUS) {
                    clearInterval(interval);
                    $statusText.addClass('label-success');
                    $infoSection.find('.fa-spin').addClass('hidden');
                    getImage(data.Results);
                }
            });
        }, JOB_INTERVAL);
    }

    $('#datasetupload').on('change', function () {
        cleanSection();
        var file = this.files[0];
        var fd = new FormData();
        fd.append('file', file);
        ajaxCall(
            {
                url: '/image/uploaddataset',
                data: fd,
                method: 'POST'
            },
            function (data) {
                var readImage = document.getElementById('previewimg');
                readImage.setAttribute('src', data.image_url);
                $('#datasefileid').val(data.dataset_name);
                $imagePreview.removeClass('hidden');
            });
    });

    $('#applyFilter').on('click', function () {
        var fd = {
            centroids: $('#centroids').val(),
            iterations: $('#iter').val(),
            datasetName: $('#datasefileid').val()
        }
        ajaxCall(
            {
                url: '/image/submitjob',
                method: 'POST',
                data: JSON.stringify(fd)
            },
            function (data) {
                getJobStatus('/image/jobstatus?jobId=' + data.job_id);
            }, true);
    });

})();
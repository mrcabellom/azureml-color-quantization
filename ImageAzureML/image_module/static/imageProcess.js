(function () {
    'use strict';

    var JOB_INTERVAL = 5000;
    var PROCESS_STATUS = 'Finished';
    var OUTPUT_PARAM = 'output_image';
    var OUTPUT_PARAM_ORIGINAL = 'original_cluster';
    var $infoSection = $('.info-section');
    var $imagePreview = $('.image-preview');
    var $statusText = $('#statusText');
    var $colorSection = $('.color-section');
    var $originalImage = $('#previewimg');
    var $colorQuantizationTemplate = $("#colorQuantization");

    function cleanSection() {
        $infoSection.addClass('hidden');
        $colorSection.find('.result-image').remove();
        $colorSection.addClass('hidden');
        $('.form-control').val('');
        $statusText.text('');
        $statusText.removeClass('label-success');
        $infoSection.find('.fa-spin').removeClass('hidden');
    }

    function getImage(blobResultData) {
        var datasetBlobInfoQuantization = blobResultData[OUTPUT_PARAM];
        var datasetBlobInfo = blobResultData[OUTPUT_PARAM_ORIGINAL];
        var urlQuantization = datasetBlobInfoQuantization.BaseLocation + datasetBlobInfoQuantization.RelativeLocation
            + datasetBlobInfoQuantization.SasBlobToken;
        var url = datasetBlobInfo.BaseLocation + datasetBlobInfo.RelativeLocation
            + datasetBlobInfo.SasBlobToken;
        var srcOriginalImage = $originalImage.attr('src');
        var originalFileName = srcOriginalImage.substring(srcOriginalImage.lastIndexOf('/') + 1);
        ajaxCall(
            {
                url: '/image/filteredimage',
                method: 'POST',
                data: JSON.stringify({ 'blobUrl': urlQuantization, 'originalUrl': url, 'originalFileName': originalFileName })
            },
            function (data) {
                $infoSection.filter('.result-image').removeClass('hidden');
                $colorSection.removeClass('hidden');
                var filteredImage = document.getElementById('filteredImage');
                filteredImage.setAttribute('src', data.images_urls[0]);
                var colorTemplate = _.template($colorQuantizationTemplate.html());
                $colorSection.append(
                    colorTemplate({ imagePaths: data.images_urls.slice(1, data.images_urls.length) })
                );
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
                $originalImage.attr('src', data.image_url);
                $('#datasetfileid').val(data.dataset_name);
                $imagePreview.removeClass('hidden');
            });
    });

    $('#applyFilter').on('click', function () {
        var fd = {
            centroids: $('#centroids').val(),
            iterations: $('#iter').val(),
            datasetName: $('#datasetfileid').val()
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

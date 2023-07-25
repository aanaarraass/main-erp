odoo.define('openeducat_attendance_face_recognition.face_control', function (require) {
    "use strict";

    async function load_models() {
        let models_path = '/openeducat_attendance_face_recognition/static/src/js/models'
        return Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri(models_path),
            faceapi.nets.faceLandmark68Net.loadFromUri(models_path),
            faceapi.nets.faceRecognitionNet.loadFromUri(models_path),
            faceapi.nets.faceExpressionNet.loadFromUri(models_path),
        ]).then((val) => {

        }).catch((err) => {

        });
    }

    var getDescriptors = (video, img) => {
        return faceapi.detectSingleFace(video || img, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceExpressions()
            .withFaceDescriptor();
    }

    function _f32base64(descriptor) {
        let f32base64 = btoa(String.fromCharCode(...(new Uint8Array(descriptor.buffer))));
        return f32base64;
    }

    return {
        load_models: load_models,
        _f32base64: _f32base64,
        getDescriptors: getDescriptors,
    }


});

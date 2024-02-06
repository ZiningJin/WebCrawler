import React, { useState } from 'react';
import axios from 'axios';
import './cceup.css'

const Cceup = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadSuccess, setUploadSucess] = useState(false);
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]); // handle single file
    };
    const handleFileUpload = async() => {
        const formData = new FormData();
        formData.append('file', selectedFile); // use file to match Backend

        try{
            const response = await axios.post('/api/cceup_upload', formData, {
                baseURL: 'http://localhost:5000',
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log(response.data);
            setUploadSucess(true);
        } catch (error){
            console.error('Error Uploading Files:', error);
            setUploadSucess(false);
        }
    };


    const [rowCount, setRowCount] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const handleProcessData = async () => {
      setIsProcessing(true);
      try {
        const response = await axios.get('/api/cceup_transform', {
          baseURL: 'http://localhost:5000'
        });
        setRowCount(response.data.row_count); // if the key in JSON Object is 'row count' it should be response.data['row count']
        setIsProcessing(false);
      } catch (error) {
        console.error('Error processing data:', error);
        setIsProcessing(false);
      }
    };

    const handleDownload = () => {
        axios({
            url: 'http://localhost:5000/api/cceup_download',
            method: 'GET',
            responseType: 'blob',
          }).then((response) => {
            // Create a URL for the blob
            const url = window.URL.createObjectURL(new Blob([response.data]));
            // Create a temporary link to trigger the download
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download','df_cceup.csv')
            document.body.appendChild(link);
            link.click();
            link.remove(); // Clean up the DOM
            window.URL.revokeObjectURL(url); // Free up memory
          }).catch((error) => {
            console.error('Error downloading the file:', error);
          })
    };

  return (
    <section id="cceup">
        <div className="container cceup__container">
            <div className="card">
                <h3>Video You Must Watch</h3>
                {/* <iframe src='' allowFullScreen title="Intro Video"></iframe> */}
                <a href="" target='_ blank' rel="noopener noreferrer">Video</a>
            </div>

            <div className="card">
                <h3>Step 1: File Upload</h3>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleFileUpload}>Upload</button>
                {uploadSuccess && <p>Upload Successfully!</p>}
            </div>

            <div className="card">
                <h3>Step2: Data Transformation</h3>
                <button onClick={handleProcessData} disabled={isProcessing}>{isProcessing ? 'Processing...' : 'Process'}</button>
                {rowCount !== null && (
                    <p>Row Count of df_cceup: {rowCount}</p>
                )}
            </div>

            <div className="card">
                <h3>Step3: Download</h3>
                <button onClick={handleDownload}>Download</button>
            </div>
        </div>
    </section>
  )
}

export default Cceup

import React, { useState } from 'react';
import axios from 'axios';
import './bci.css';

const Bci = () => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploadSuccess, setUploadSucess] = useState(false);
    const handleFileChange = (event) => {
        setSelectedFiles(event.target.files);
    };
    const handleFileUpload = async() => {
        const formData = new FormData();
        for (let file of selectedFiles){
            formData.append('files', file);
        }

        try{
            const response = await axios.post('/api/bci_upload', formData, {
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

    const [rowCountPrev, setRowCountPrev] = useState(null);
    const [isProcessingPrev, setIsProcessingPrev] = useState(false);
    const handleProcessData = async () => {
      setIsProcessingPrev(true);
      try {
        const response = await axios.get('/api/bci_concat', {
          baseURL: 'http://localhost:5000'
        });
        setRowCountPrev(response.data.row_count);
        setIsProcessingPrev(false);
      } catch (error) {
        console.error('Error processing data:', error);
        setIsProcessingPrev(false);
      }
    };

    const [rowCount, setRowCount] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleDedupAndUpdate = async () => {
      setIsProcessing(true);
      try {
        const response = await axios.get('/api/bci_dedup_update', {
          baseURL: 'http://localhost:5000'
        });
        setRowCount(response.data.row_count);
        setIsProcessing(false);
      } catch (error) {
        console.error('Error processing data:', error);
        setIsProcessing(false);
      }
    };

    const handleDownload = () => {
      axios({
        url: 'http://localhost:5000/api/bci_download_archive',
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        // Create a URL for the blob
        const url = window.URL.createObjectURL(new Blob([response.data]));
        // Create a temporary link to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download','bci_uniqueids_tbl_archive.csv')
        document.body.appendChild(link);
        link.click();
        link.remove(); // Clean up the DOM
        window.URL.revokeObjectURL(url); // Free up memory
      }).catch((error) => {
        console.error('Error downloading the file:', error);
      })
    };

    const handleTransformDownload = () => {
      axios({
        url: 'http://localhost:5000/api/bci_transform',
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        // Create a URL for the blob
        const url = window.URL.createObjectURL(new Blob([response.data]));
        // Create a temporary link to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download','bci_dfs_unique.csv')
        document.body.appendChild(link);
        link.click();
        link.remove(); // Clean up the DOM
        window.URL.revokeObjectURL(url); // Free up memory
      }).catch((error) => {
        console.error('Error downloading the file:', error);
      })
    };
  

  return (
    <section id='bci'>
      <div className="container bci__container">
        <div className="card">
            <h3>Video You MUST Watch</h3>
            {/* <iframe src='' allowFullScreen title="Intro Video"></iframe> */}
            <a href="https://irglobal-my.sharepoint.com/:v:/g/personal/charlie_jin_irco_com/EVH_sNqyCZBNjNTR2ITvqEQBe14FwwrmXml8JmFluBGZGQ" target='_ blank' rel="noopener noreferrer">Video</a>
          </div>

          <div className="card">
            <h3>Step 1: File Upload</h3>
            <input type="file" multiple onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>
            {uploadSuccess && <p>Upload Successfully!</p>}
          </div>
          
          <div className="card">
            <h3>Step 2: Data Concatenation and Processing</h3>
            <button onClick={handleProcessData} disabled={isProcessingPrev}>{isProcessingPrev ? 'Processing...' : 'Process'}</button>
            {rowCountPrev !== null && (
            <p>Row Count of dfs_concat: {rowCountPrev}</p>
          )}
          </div>

          <div className="card">
            <h3>Step 3_4: Deduplicate and Update</h3>
            <button onClick={handleDedupAndUpdate} disabled={isProcessing}>{isProcessing ? 'Processing...' : 'Process'}</button>
            {rowCount !== null && (
              <p>Row Count of dfs_unique: {rowCount}</p>
            )}
          </div>

          <div className="card">
            <h3>Step 5_6: Data Transformation and Download</h3>
            <button onClick={handleTransformDownload}>Download</button>
          </div>

          <div className="card">
            <h3>Step 7: Download Archived ProjectIDs</h3>
            <button onClick={handleDownload}>Download</button>
          </div>

      </div>
    </section>
  )
}

export default Bci

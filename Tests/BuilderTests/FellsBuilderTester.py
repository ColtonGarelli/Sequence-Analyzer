import unittest
import json
import requests as r
from Builders.AnalysisBuilders import FELLSAnalysisBuilder
from Bio import Seq
from Bio.SeqRecord import SeqRecord


class FELLSAPITester(unittest.TestCase):

    fells_builder = FELLSAnalysisBuilder()
    test_jobid = "5acb64e20fe7e54308d3f853"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    fasta_formatted = "\n>ID_0\nMVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR" \
                      "\n>ID_1\nMVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR" \
                      "\n>ID_2\nASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD"

    # tests formatting from a list of seq_records
    # need to test converting strings to seqrecords

    # TODO: gotta implement more boundary cases with sequence variation
    # TODO: test+implement error handling for improper formatting by creating errors for when a submission fails (read a response and check for error status
    # TODO: copy requests to a test helper file and read file in to test request decoding
    # TODO:

    def pre_test_setup(self):
        """***Precondition function***
        Creates a list of SeqRecords to be used for testing
        Returns:
        """
        seq_record1 = SeqRecord(description="", id="ID_0", seq=Seq.Seq(
            "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"))
        seq_record2 = SeqRecord(description="", id="ID_1", seq=Seq.Seq(
            "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"))
        seq_record3 = SeqRecord(description="", id="ID_2", seq=Seq.Seq("ASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD"))
        seq_record_list = [seq_record1, seq_record2, seq_record3]
        return seq_record_list

    def seqrecord_to_fasta(self, seqrecord_list):
        """***Precondition function***
        Converts a SeqRecord list into proper format for submitting to the FELLS API

        Args:
            seqrecord_list: a list of SeqRecords

        Returns: A properly formatted string intended for the body of a FELLS API request

        """
        test_body_str = "\n\n"
        for i in seqrecord_list:
            test_body_str = test_body_str + i.format("fasta") + "\n\n"
        test_body_str = test_body_str[0:(test_body_str.__len__()-1)]
        return test_body_str

    def test_formatting_body(self):
        seqrecord_list = self.pre_test_setup()
        test_body_str = self.seqrecord_to_fasta(seqrecord_list)
        actual_body = self.fells_builder.format_body_for_processing([i.format('fasta') for i in seqrecord_list])
        self.assertEqual(test_body_str, actual_body, "fellsbuilder.format_body_for_processing failed to format fasta"
                                                     "string list properly")

    def test_preparing_request(self):
        """***TEST***

        Returns:

        """
        seqrecord_list = self.pre_test_setup()
        test_body_str = self.seqrecord_to_fasta(seqrecord_list)
        json_str = json.dumps({"sequence": test_body_str}).encode()
        prepped_req = self.fells_builder.prepare_request(seqrecord_list)
        test_prepped = r.Request(method='POST', headers=self.headers, data=json_str, url="http://protein.bio.unipd.it/fellsws/submit")
        test_prepped = test_prepped.prepare()
        self.assertEqual(json_str, prepped_req.body, "Body not properly formatted")
        self.assertEqual(test_prepped.headers, prepped_req.headers, "Error formatting headers")

    def test_data_integrity_in_request(self):
        """***TEST***

        Returns:

        """
        seqrecord_list = self.pre_test_setup()
        test_body_str = self.seqrecord_to_fasta(seqrecord_list)
        prepped_req = self.fells_builder.prepare_request(seqrecord_list)
        json_str = json.dumps({"sequence": test_body_str}).encode()
        test_prepped = r.Request(method='POST', headers=self.headers, data=json_str, url="http://protein.bio.unipd.it/fellsws/submit")
        test_prepped = test_prepped.prepare()
        json_body = json.loads(prepped_req.body)
        self.assertEqual(test_body_str, json_body['sequence'], "Sequence data not properly formatted in request")
        # fasta_list = ["MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR",
        #               "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR",
        #               "ASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD"]
        # prepped_req = self.fells_builder.prepare_request(fasta_list)
        # self.assertEqual(test_prepped.body, prepped_req.body)

    def test_check_submission_status(self):
        """***TEST***
        Checks an existing job to ensure a job status response is retrieved and properly parsed

        """
        base_url = "http://protein.bio.unipd.it/fellsws/status/"
        # TODO: Make a precondition function that checks the status of the job and returns the response content
        check_status = self.fells_builder.check_status(self.test_jobid)
        # ensures that existing request is accessed correctly (and still exists)
        self.assertTrue(check_status.ok)
        json_data = check_status.content.decode('utf-8')
        json_parsed = json.loads(json_data)
        if 'status' in json_parsed:
            status = True
        else:
            status = False
        self.assertTrue(status, "response object does not contain 'status' field. ")
        status = json_parsed['status']
        # check to make sure status is done (which it should barring an issue)
        self.assertEqual("done", status)
        check_status.close()

    def test_check_processing_status(self):
        """***TEST***

        Returns:

        """
        check_status = self.fells_builder.check_status(self.test_jobid)
        json_data = check_status.content.decode('utf-8')
        json_parsed = json.loads(json_data)
        if ['names'][0][0] in json_parsed:
            has_names = True
        else:
            has_names = False
        self.assertTrue(has_names, "The response has no 'names' field")
        names = json_parsed['names'][0][1]
        processing_status = self.fells_builder.check_processing_status(names)
        self.assertTrue(processing_status, "Processing status came back false. Problem with format of request sent")



    # make a sequence object and translate to fasta
    # or make fasta strings for testing
    # check that the response is good (200) and make sure it contains a request ID
    # def test_prepare_request

    # TODO: test transferring data to SeqRecord annotations
    def test_update_annotations(self):
        """***TEST***


        """
        self.assertEqual(True, True)

    def test_prep_for_viewing(self):
        pass


if __name__ == '__main__':
    unittest.main()

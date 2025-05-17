import React from "react";
import { Container, Row, Col } from "shards-react";

import PageTitle from "../components/common/PageTitle";
import Nothando from "../components/patient-profile/Nothando";
import Mxolisi from "../components/patient-profile/Mxolisi";
import Palesa from "../components/patient-profile/Palesa";
import Dumisani from "../components/patient-profile/Dumisani";


const MyPatients = () => (
    <Container fluid className="main-content-container px-4">
    <Row noGutters className="page-header py-4">
      <PageTitle title="Patient List" subtitle="My Patients" md="12" className="ml-sm-auto mr-sm-auto" />
    </Row>
    <Row>
      <Col lg="3">
        <Palesa/>
      </Col>
      <Col lg="3">
        <Dumisani/>
      </Col>
      <Col lg="3">
        <Mxolisi/>
      </Col>
      <Col lg="3">
        <Nothando/>
      </Col>
    </Row>
  </Container>
);

export default MyPatients;

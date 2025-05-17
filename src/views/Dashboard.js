import React from "react";
import { Button, Container, Row, Col, Card, CardHeader, CardBody } from "shards-react";
import { Link } from "react-router-dom";

import PageTitle from "../components/common/PageTitle";

const Dashboard = () => (
  <Container fluid className="main-content-container px-4">
    {/* Page Header */}
    <Row noGutters className="page-header py-4">
      <PageTitle sm="4" title="Live Cases" subtitle="Cases Now" className="text-sm-left" />
    </Row>

    {/* Default Light Table */}
    <Row>
      <Col>
        <Card small className="mb-4">
          <CardHeader className="border-bottom">
          </CardHeader>
          <CardBody className="p-0 pb-3">
            <table className="table mb-0">
              <thead className="bg-light">
                <tr>
                  <th scope="col" className="border-0">PID</th>
                  <th scope="col" className="border-0">Name</th>
                  <th scope="col" className="border-0">Sex</th>
                  <th scope="col" className="border-0">Category</th>
                  <th scope="col" className="border-0">Description</th>
                  <th scope="col" className="border-0">Time Log</th>
                  <th scope="col" className="border-0">Prev History</th>
                  <th scope="col" className="border-0">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>Thabiso</td>
                  <td>Male</td>
                  <td>Cardiologist</td>
                  <td>Severe chest pain and shortness of breath suspected to be myocardial infarction</td>
                  <td>1 month ago</td>
                  <td>Yes</td>
                  <td>
                    <Button tag={Link} to="mypatients" outline theme="success" className="mb-2 mr-1">
                      Accept
                    </Button>
                  </td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>Zanele</td>
                  <td>Female</td>
                  <td>Neurologist</td>
                  <td>Sudden loss of consciousness with suspected stroke symptoms</td>
                  <td>2 hours ago</td>
                  <td>No</td>
                  <td>
                    <Button tag={Link} to="mypatients" outline theme="success" className="mb-2 mr-1">
                      Accept
                    </Button>
                  </td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>Lebogang</td>
                  <td>Female</td>
                  <td>General Practitioner</td>
                  <td>Complaints of high fever, fatigue, and rash – suspected viral infection</td>
                  <td>2 days ago</td>
                  <td>Yes</td>
                  <td>
                    <Button tag={Link} to="mypatients" outline theme="success" className="mb-2 mr-1">
                      Accept
                    </Button>
                  </td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>Sipho</td>
                  <td>Male</td>
                  <td>Pulmonologist</td>
                  <td>Difficulty breathing and persistent cough – possible pneumonia case</td>
                  <td>23 hours ago</td>
                  <td>No</td>
                  <td>
                    <Button tag={Link} to="mypatients" outline theme="success" className="mb-2 mr-1">
                      Accept
                    </Button>
                  </td>
                </tr>
              </tbody>
            </table>
          </CardBody>
        </Card>
      </Col>
    </Row>
  </Container>
);

export default Dashboard;

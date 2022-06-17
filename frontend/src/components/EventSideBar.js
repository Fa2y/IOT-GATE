import React from "react";
import { UncontrolledCollapse, Button, Alert, Container } from "reactstrap";
import { DateTime } from "luxon";

const EventSideBar = ({ alerts }) => {
  // const events = [{ color: "success", title: "Hello", content: "World" }];
  return (
    <div className="mx-1 mt-1">
      <Button
        style={{ zIndex: "10", height: "50px", width: "100px" }}
        id="toggler"
        color="primary"
      >
        Event Log
      </Button>
      <UncontrolledCollapse toggler="#toggler">
        <Container
          className="py-1"
          style={{
            backgroundColor: "lightgray",
            width: "300px",
            height: "600px",
            borderRadius: "10px",
            overflowY: "scroll",
          }}
        >
          {alerts &&
            Object.entries(alerts)
              ?.sort(
                (a1, a2) =>
                  Number.parseInt(a2[0].split("-")[0]) -
                  Number.parseInt(a1[0].split("-")[0])
              )
              ?.map((alert) => (
                <Alert
                  color="danger"
                  className="my-2"
                  style={{
                    boxShadow: "4px 3px 10px 0px #999999",
                    fontSize: "14px",
                  }}
                >
                  <h6 className="alert-heading">{`Attack from ${alert[1]?.alert_host}`}</h6>
                  <hr className="my-0" />
                  <p className="mb-0">
                    <b>Details: </b>
                    {alert[1]?.alert_details}
                  </p>
                  <small>
                    {`Date and Time: ${DateTime.fromSeconds(
                      Number.parseInt(alert[0].split("-")[0]) / 1000
                    ).toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS)}`}
                  </small>
                </Alert>
              ))}
        </Container>
      </UncontrolledCollapse>
    </div>
  );
};

export default EventSideBar;

import React from "react";
import { UncontrolledCollapse, Button, Alert, Container } from "reactstrap";

const EventSideBar = () => {
  const events = [{ color: "success", title: "Hello", content: "World" }];
  return (
    <div className="mx-1">
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
          }}
        >
          {events?.map((event) => (
            <Alert
              color={event?.color}
              className="my-2"
              style={{ boxShadow: "4px 3px 10px 0px #999999" }}
            >
              <h4 className="alert-heading">{event?.title}</h4>
              <hr />
              <p className="mb-0">{event?.content}</p>
            </Alert>
          ))}
        </Container>
      </UncontrolledCollapse>
    </div>
  );
};

export default EventSideBar;

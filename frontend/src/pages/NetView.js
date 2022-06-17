import React, { useState, useEffect } from "react";
import Graph from "react-graph-vis";
import EventSideBar from "components/EventSideBar";
import { Button } from "reactstrap";
import Slider from "react-rangeslider";
import logoName from "../assests/imgs/IOTprint_wname.png";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { API_BASE_URL } from "../constants";
import { DateTime } from "luxon";
import { toast } from "react-toastify";
import LoadingOverlay from "react-loading-overlay";

const NetView = () => {
  const [data, setData] = useState(null);
  const [network, setNetwork] = useState(null);
  const [hostNodes, setHostNodes] = useState([]);
  const [hostEdges, setHostEdges] = useState([]);
  const [timestampShift, setTimestampShift] = useState(0);
  const [level, setLevel] = useState(1000);
  const [isLive, setIsLive] = useState(true);
  const [alerts, setAlerts] = useState(null);
  const [loading, setLoading] = useState(true);
  const historyTime = 30 * 60 * 1000; // 30min in millisec
  const { sendMessage, lastMessage, readyState } = useWebSocket(
    `ws://${API_BASE_URL["dev"]}/netview-ws`
  );
  const { lastMessage: alertLastMessage } = useWebSocket(
    `ws://${API_BASE_URL["dev"]}/alerts-ws`
  );
  const options = {
    physics: {
      stabilization: false,
    },
    nodes: {
      color: "#53BF9D",
    },
    edges: {
      physics: false,
      color: "#233b91",
      arrows: {
        to: {
          enabled: true,
          type: "arrow",
        },

        from: {
          enabled: true,
          type: "arrow",
        },
      },
      length: 200,
    },
    height: "100%",
    width: "100%",
  };

  const events = {
    select: function (event) {
      // var { nodes, edges } = event;
    },
  };

  const handleTimeStampChange = (value) => {
    setIsLive(false);
    setLevel(value);
  };
  const drawNotifs = (data) => {
    Object.values(data).forEach((notif) =>
      toast.error(`Malicious activity detected from host:${notif?.alert_host}`)
    );
  };

  useEffect(() => {
    const markAttacker = (attacker_hosts) => {
      const newHostNodes = hostNodes?.map((host) =>
        attacker_hosts?.includes(host?.label)
          ? { ...host, color: "#dc3545" }
          : host
      );
      setHostNodes(newHostNodes);
    };
    if (alerts) {
      markAttacker(Object.values(alerts).map((alert) => alert?.alert_host));
    }
  }, [alerts]);

  useEffect(() => {
    if (alertLastMessage) {
      const recvData = JSON.parse(alertLastMessage?.data);
      if (Object.values(recvData).length === 1) {
        drawNotifs(recvData);
      }
      console.log("Data recvied");
      console.log(recvData);
      setAlerts((alerts) => ({
        ...alerts,
        ...recvData,
      }));
    }
  }, [alertLastMessage]);

  useEffect(() => {
    if (lastMessage) setData(JSON.parse(lastMessage?.data));
  }, [lastMessage]);

  useEffect(() => {
    if (isLive && ReadyState.OPEN === readyState) {
      setLoading(true);
      sendMessage("latest");
    }
  }, [isLive, readyState, sendMessage]);

  useEffect(() => {
    if (ReadyState.OPEN === readyState) {
      setLoading(true);
      sendMessage(timestampShift);
    }
  }, [timestampShift, readyState, sendMessage]);

  useEffect(() => {
    if (data) {
      if (data?.hosts?.length > 0) {
        setHostNodes(
          data?.hosts?.map((host, index) => ({
            id: index,
            label: host,
            title: "HELLOWORLD",
          }))
        );
      }
      if (data?.connections?.length > 0) {
        setHostEdges(
          data?.connections?.map((edge) => ({
            from: data?.hosts?.indexOf(edge?.split("-")[0]),
            to: data?.hosts?.indexOf(edge?.split("-")[1]),
          }))
        );
      }
      setLoading(false);
      if (network) network?.stabilize();
    }
  }, [data]);

  const handleTimeStampFinishChange = (value) => {
    setTimestampShift(((1000 - level) * historyTime) / 1000);
  };

  return (
    <>
      {/* <div
        className="w-50 mt-2"
        style={{ zIndex: "10", position: "fixed", left: "25%", opacity: "90%" }}
      >
        {notifications?.map((notif) => (
          <UncontrolledAlert color="danger">{notif}</UncontrolledAlert>
        ))}
      </div> */}
      <div className="d-flex ">
        <EventSideBar alerts={alerts} />
        <div>
          <LoadingOverlay
            active={loading}
            spinner
            text="Fetching Data and Drawing..."
          >
            <Graph
              style={{
                height: "600px",
                borderRadius: "10px",
                borderStyle: "solid",
                borderColor: "#233b91",
              }}
              graph={{ nodes: hostNodes, edges: hostEdges }}
              options={options}
              events={events}
              getNetwork={(netw) => {
                if (network === null) setNetwork(netw);
              }}
            />
          </LoadingOverlay>
          <div className="d-flex justify-content-between align-items-center">
            <Slider
              className="w-100"
              min={0}
              max={1000}
              tooltip={false}
              value={level}
              onChange={handleTimeStampChange}
              onChangeComplete={handleTimeStampFinishChange}
            />
            <Button
              style={{ width: "70px" }}
              className="d-flex align-items-center justify-content-around px-1 mx-1"
              onClick={(e) => {
                e.preventDefault();
                setIsLive(true);
                setLevel(1000);
                setTimestampShift(0);
              }}
              active={isLive}
              outline={isLive}
              color="primary"
            >
              <div
                style={{
                  borderRadius: "50%",
                  width: "10px",
                  height: "10px",
                  backgroundColor: "red",
                }}
              ></div>
              Live
            </Button>
            <img
              alt="logo-withname"
              src={logoName}
              style={{ width: "80px", float: "right" }}
            />
          </div>
          <p className="text-center">
            <b> Date:</b>
            {` ${DateTime.fromSeconds(
              DateTime.now().toUnixInteger() - timestampShift
            ).toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS)}`}
          </p>
        </div>
      </div>
    </>
  );
};

export default NetView;

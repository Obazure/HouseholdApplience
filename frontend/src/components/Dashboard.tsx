import React, {FC, useEffect, useState} from 'react'
import {Card, Col, Row} from "antd"
import {useQuery} from "react-query"
import {apiGetQueries} from "../utils/api"
import {NewQueryInterface, QueryInterface} from "../models/interfaces"
import QueryCard from "./QueryCard";
import ResultCard from "./ResultCard";
import QueryHistoryCard from "./QueryHistoryCard";

const Dashboard: FC = () => {

    const {isLoading, error, data} = useQuery("getQueries",
        async () => await apiGetQueries()
    );
    const [apiLoadingStatus, setLoadingStatus] = useState(false)
    useEffect(() => {
        setLoadingStatus(isLoading)
    }, [isLoading])


    const queriesInitial: QueryInterface[] = []
    const queryInitial: QueryInterface | NewQueryInterface = {query: '', query_hash: ''}
    const [queries, setQueries] = useState(queriesInitial)
    const [currentQuery, setCurrentQuery] = useState(queryInitial)


    useEffect(() => {
        if (data && Array.isArray(data)) {
            setQueries(data)
        } else {
            setQueries(queriesInitial)
        }
    }, [data])


    return (
        <Row className="padding">
            <Col span={16} className="padding">
                <Row>
                    <Col span={24}>
                        <Card title="New Request">
                            <QueryCard
                                items={queries}
                                onItemsChange={setQueries}
                                item={currentQuery}
                                onItemChange={setCurrentQuery}
                                isLoading={apiLoadingStatus}
                            />
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card title="Query Result">
                            <ResultCard
                                items={queries}
                                onItemsChange={setQueries}
                                item={currentQuery}
                                onItemChange={setCurrentQuery}
                                isLoading={apiLoadingStatus}
                            />
                        </Card>
                    </Col>
                </Row>
            </Col>
            <Col span={8} className="padding">
                <Card title="Query History">
                    <QueryHistoryCard
                        items={queries}
                        onItemsChange={setQueries}
                        item={currentQuery}
                        onItemChange={setCurrentQuery}
                        isLoading={apiLoadingStatus}
                    />
                </Card>
            </Col>
        </Row>
    )
}

export default Dashboard
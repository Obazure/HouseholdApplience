import {Dispatch, SetStateAction} from "react";


export interface CardPropsInterface {
    items: QueryInterface[],
    onItemsChange: Dispatch<SetStateAction<QueryInterface[]>>,
    item: QueryInterface | NewQueryInterface,
    onItemChange: Dispatch<SetStateAction<QueryInterface | NewQueryInterface>>,
    isLoading?: boolean
}

export interface NewQueryInterface {
    query: string
    query_hash: string
}

export interface QueryInterface {
    id: number,
    created_at: string,
    updated_at: string,
    query: string,
    query_hash: string,
    articles?: ArticleInterface[]
}

export interface ArticleInterface {

    id: number,
    created_at: string,
    updated_at: string,
    source_url: string,
    source_url_hash: string,
    source_tag: string,
    published_at: string,
    title: string,
    read_url: string,
    content: string,
    categories?: CategoryInterface[],
    result?: ResultInterface
}

export interface CategoryInterface {

    id: number,
    created_at: string,
    updated_at: string,
    name: string,
    tag: string,
}

export interface ResultInterface {
    total_words: number,
    total_sentences: number,
    most_frequent_words?: Map<string, number>
}
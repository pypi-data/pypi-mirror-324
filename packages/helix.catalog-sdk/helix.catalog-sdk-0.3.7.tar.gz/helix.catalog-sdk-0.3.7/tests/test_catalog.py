import datetime
import json
import os.path
import shutil
from types import ModuleType
from typing import Dict, Optional, List

from helix_catalog_sdk.catalog import Catalog
from helix_catalog_sdk.data_source import LastProcessed
from helix_catalog_sdk.repo import DirectoryRepo
from helix_catalog_sdk.enums import HelixEnvironment

TEST_DIR = os.path.dirname(__file__)
SOURCE_CATALOG = os.path.join(TEST_DIR, "test_catalog")
SOURCE_DATA = os.path.join(TEST_DIR, "test_data")


def clean_test_folder() -> None:
    shutil.rmtree("catalog", ignore_errors=True)
    shutil.rmtree("data", ignore_errors=True)
    print("Setting up")
    print(" * Copying directory 'test_catalog' to 'catalog' for testing")
    shutil.copytree(src=SOURCE_CATALOG, dst="catalog")
    shutil.copytree(src=SOURCE_DATA, dst="data")


def setup_module(module: ModuleType) -> None:
    clean_test_folder()


def teardown_module(module: ModuleType) -> None:
    print("Tearing down")
    print(" * Removing directory 'catalog'")
    shutil.rmtree("catalog", ignore_errors=True)
    shutil.rmtree("data", ignore_errors=True)


def test_catalog_get_data_source() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)

    data_source = catalog.get_data_source(
        "catalog/raw/gencon/icd.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None

    assert (
        data_source.base_connection_formatted == "s3://prod-ingestion/raw/gencon/icd/"
    )
    assert len(data_source.resources) == 3

    people_resource = data_source.resources[0]
    assert people_resource.name == "people"
    assert (
        people_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json"
    )
    assert people_resource.last_processed is not None
    assert (
        people_resource.last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json"
    )
    people_resource.last_processed.set_last_processed(
        "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092022.json",
        HelixEnvironment.PRODUCTION,
    )
    assert (
        people_resource.last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092022.json"
    )

    places_resource = data_source.resources[1]
    assert places_resource.name == "places"
    assert (
        places_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/Places/PlaceFeed_06172021.json"
    )

    things_resource = data_source.resources[2]
    assert things_resource.name == "things"
    assert (
        things_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/Things/ThingFeed_06092021.json"
    )

    assert len(data_source.pipeline_subscriptions) == 4
    pipeline_subscription = data_source.pipeline_subscriptions[0]
    assert pipeline_subscription.flow_name == "Simple subscription"
    assert pipeline_subscription.flow_parameters == []

    pipeline_subscription = data_source.pipeline_subscriptions[1]
    assert pipeline_subscription.flow_name == "INGEN Data Ingestion"
    assert pipeline_subscription.flow_parameters == ["people", "places"]

    pipeline_subscription = data_source.pipeline_subscriptions[2]
    assert pipeline_subscription.flow_name == "Test Flow"
    assert len(pipeline_subscription.flow_parameters) == 0
    assert pipeline_subscription.flow_parameters == []

    pipeline_subscription = data_source.pipeline_subscriptions[3]
    assert pipeline_subscription.flow_name == "Prefect Flow"
    assert pipeline_subscription.flow_parameters == ["places"]
    assert pipeline_subscription.deployment_name == "Deployment Name"

    assert data_source.connection_type == "file"


def test_catalog_update_data_source_resource_with_links() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/thedacare_uhccomm/TCACO_ccv_mask_202203.csv"
    )

    assert updated_data_sources is not None
    assert len(updated_data_sources[0].resources) == 3
    thedacare_united_commercial_aco_claims = updated_data_sources[0].resources[0]
    assert (
        thedacare_united_commercial_aco_claims.name
        == "thedacare_united_commercial_aco_claims"
    )
    assert (
        thedacare_united_commercial_aco_claims.full_path
        == "s3://bwell-ingestion/preprocessed/thedacare_uhccomm/TCACO_ccv_mask_202203.csv"
    )
    assert thedacare_united_commercial_aco_claims.linked_group == "alpha"


def test_catalog_update_data_source_resource() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    updated_data_sourcess = catalog.update_data_source_resource(
        "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06142021.json"
    )

    assert updated_data_sourcess is not None

    assert (
        updated_data_sourcess[0].base_connection_formatted
        == "s3://prod-ingestion/raw/gencon/icd/"
    )
    assert len(updated_data_sourcess[0].resources) == 3

    people_resource = updated_data_sourcess[0].resources[0]
    assert people_resource.name == "people"
    assert (
        people_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06142021.json"
    )

    places_resource = updated_data_sourcess[0].resources[1]
    assert places_resource.name == "places"
    assert (
        places_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/Places/PlaceFeed_06172021.json"
    )

    things_resource = updated_data_sourcess[0].resources[2]
    assert things_resource.name == "things"
    assert (
        things_resource.full_path
        == "s3://prod-ingestion/raw/gencon/icd/Things/ThingFeed_06092021.json"
    )

    assert len(updated_data_sourcess[0].pipeline_subscriptions) == 4
    pipeline_subscription = updated_data_sourcess[0].pipeline_subscriptions[0]
    assert pipeline_subscription.flow_name == "Simple subscription"
    assert pipeline_subscription.flow_parameters == []

    pipeline_subscription = updated_data_sourcess[0].pipeline_subscriptions[1]
    assert pipeline_subscription.flow_name == "INGEN Data Ingestion"
    assert pipeline_subscription.flow_parameters == ["people", "places"]

    pipeline_subscription = updated_data_sourcess[0].pipeline_subscriptions[2]
    assert pipeline_subscription.flow_name == "Test Flow"
    assert len(pipeline_subscription.flow_parameters) == 0
    assert pipeline_subscription.flow_parameters == []

    assert updated_data_sourcess[0].connection_type == "file"

    # Load json from file for comparison as well, not just from in-memory object and confirm data properly updated
    json_file = "catalog/raw/gencon/icd.json"
    json_data = json.load(open(json_file))
    json_resources = json_data.get("resources")
    assert json_resources == [
        {
            "load_folders": False,
            "last_processed": {
                "dev": "s3://dev-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json",
                "production": "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json",
                "qa": "",
                "staging": "s3://staging-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json",
                "client_sandbox": "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092021.json",
            },
            "name": "people",
            "path": "People/PeopleFeed_06142021.json",
            "path_slug": "People/PeopleFeed_",
            "date_segment": None,
            "date_format": None,
            "linked_group": None,
            "linked_regex": None,
            "file_regex": None,
        },
        {
            "load_folders": False,
            "last_processed": None,
            "name": "places",
            "path": "Places/PlaceFeed_06172021.json",
            "path_slug": "Places/PlaceFeed_",
            "date_segment": None,
            "date_format": None,
            "linked_group": None,
            "linked_regex": None,
            "file_regex": None,
        },
        {
            "load_folders": False,
            "last_processed": None,
            "name": "things",
            "path": "Things/ThingFeed_06092021.json",
            "path_slug": "Things/ThingFeed_",
            "date_segment": None,
            "date_format": None,
            "linked_group": None,
            "linked_regex": None,
            "file_regex": None,
        },
    ]


def test_catalog_update_data_source_resource_with_extension() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/burris_highmark_claims_medical/20210915_2645841001FLX.txt"
    )

    assert updated_data_sources is not None
    claims_resource = updated_data_sources[0].resources[0]
    assert claims_resource.name == "burris_highmark_claims_medical"
    assert (
        claims_resource.full_path
        == "s3://bwell-ingestion/preprocessed/burris_highmark_claims_medical/20210915_2645841001FLX.txt"
    )

    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/burris_highmark_claims_medical/20210916_2645841001FLX.txt.gz"
    )

    assert updated_data_sources is None

    data_source = catalog.get_data_source(
        "catalog/preprocessed/burris/highmark/claims_medical.json",
        HelixEnvironment.PRODUCTION,
    )
    assert data_source is not None
    claims_resource = data_source.resources[0]
    assert (
        claims_resource.full_path
        == "s3://bwell-ingestion/preprocessed/burris_highmark_claims_medical/20210915_2645841001FLX.txt"
    )


def test_catalog_update_data_source_resource_with_same_directory_name() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/altrua_manifestrx_claims_rx/manifestrx_654321.csv"
    )

    assert updated_data_sources is not None
    claims_resource = updated_data_sources[0].resources[0]
    assert (
        claims_resource.full_path
        == "s3://bwell-ingestion/preprocessed/altrua_manifestrx_claims_rx/manifestrx_654321.csv"
    )
    assert claims_resource.path == "manifestrx_654321.csv"


def test_catalog_update_data_source_with_file_regex() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    # test for matching pattern with file name
    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/thedacare_anthem/ThedaCare_member_10102023.csv"
    )
    assert updated_data_sources is not None
    eligibility_resource = updated_data_sources[0].resources[0]
    assert (
        eligibility_resource.full_path
        == "s3://bwell-ingestion/preprocessed/thedacare_anthem/ThedaCare_member_10102023.csv"
    )

    # test for unmatched pattern with file name
    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/thedacare_anthem/ThedaCare_member_eligibility_10102023.csv"
    )
    assert updated_data_sources is None

    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/preprocessed/thedacare_anthem/ThedaCare_member_10102023_ctl.csv"
    )
    assert updated_data_sources is None


def test_catalog_update_data_source_with_multiple_resource() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    # test for getting multiple resources in case of same file path present in multiple catalog file
    updated_data_sources = catalog.update_data_source_resource(
        "s3://bwell-ingestion/raw/thedacare/epic/rostermemberfact/RosterMemberFact_111222.json"
    )
    assert updated_data_sources is not None
    assert len(updated_data_sources) == 2
    catalog_file_paths = [updated_data_sources[0].name, updated_data_sources[1].name]

    assert (
        "catalog/preprocessed/thedacare/anthem/aco/roster_file.json"
        in catalog_file_paths
    )
    assert (
        "catalog/preprocessed/thedacare/anthem/aco/eligibility.json"
        in catalog_file_paths
    )


def test_catalog_update_data_source_resource_returns_none() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    catalog.get_all_data_sources()

    updated_data_sources = catalog.update_data_source_resource(
        "s3://prod-ingestion/raw/gencon/icd/test/does_not_exist.csv"
    )
    assert updated_data_sources is None


def test_catalog_update_resource_last_processed() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/raw/gencon/icd.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    catalog.update_resource_last_processed(
        "people",
        "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092022.json",
        data_source,
        HelixEnvironment.PRODUCTION,
    )
    data_source = catalog.get_data_source(
        "catalog/raw/gencon/icd.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed = people_resource.last_processed
    assert last_processed is not None
    assert (
        last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "s3://prod-ingestion/raw/gencon/icd/People/PeopleFeed_06092022.json"
    )


def test_catalog_update_resource_last_processed_date_for_single_segment() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/raw/thedacare/betteru.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    catalog.update_resource_last_processed_date_segment(
        "betteru",
        datetime.datetime.strptime("2021-11-11", "%Y-%m-%d"),
        data_source,
        HelixEnvironment.PRODUCTION,
    )
    data_source = catalog.get_data_source(
        "catalog/raw/thedacare/betteru.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed = people_resource.last_processed
    assert last_processed is not None
    assert (
        last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "data/raw/thedacare/betteru/2021-11-11/patient-files/some-patient-file.csv"
    )


def test_catalog_update_resource_last_processed_date_for_multiple_segments() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    catalog.update_resource_last_processed_date_segment(
        "2095895",
        datetime.datetime.strptime("2021-11-11", "%Y-%m-%d"),
        data_source,
        HelixEnvironment.PRODUCTION,
    )
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed = people_resource.last_processed
    assert last_processed is not None
    assert (
        last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "data/events/2095895/2021/11/11/full_day/some-patient-file.csv"
    )


def test_catalog_get_resource_unprocessed_directories() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/raw/thedacare/betteru.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    paths_to_process = catalog.get_resource_unprocessed_directories(
        "betteru", data_source, HelixEnvironment.PRODUCTION
    )
    assert len(paths_to_process) == 2
    assert paths_to_process == [
        "data/raw/thedacare/betteru/2021-07-02/some-patient-file.csv",
        "data/raw/thedacare/betteru/2021-07-05/some-patient-file.csv",
    ]
    catalog.update_resource_last_processed(
        "betteru", paths_to_process[0], data_source, HelixEnvironment.PRODUCTION
    )
    paths_to_process = catalog.get_resource_unprocessed_directories(
        "betteru", data_source, HelixEnvironment.PRODUCTION
    )
    assert len(paths_to_process) == 1
    assert paths_to_process == [
        "data/raw/thedacare/betteru/2021-07-05/some-patient-file.csv"
    ]


def test_catalog_get_resource_unprocessed_directories_segments() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    paths_to_process = catalog.get_resource_unprocessed_directories(
        "2095895", data_source, HelixEnvironment.PRODUCTION
    )
    assert len(paths_to_process) == 2
    assert paths_to_process == [
        "data/events/2095895/2021/10/02/some-patient-file.csv",
        "data/events/2095895/2021/10/03/some-patient-file.csv",
    ]


def test_catalog_get_resource_last_processed_date_for_single_segment() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/raw/thedacare/betteru.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    catalog.update_resource_last_processed_date_segment(
        "betteru",
        datetime.datetime.strptime("2021-11-11", "%Y-%m-%d"),
        data_source,
        HelixEnvironment.PRODUCTION,
    )
    data_source = catalog.get_data_source(
        "catalog/raw/thedacare/betteru.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed: Optional[LastProcessed] = people_resource.last_processed
    assert last_processed is not None
    assert (
        last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "data/raw/thedacare/betteru/2021-11-11/patient-files/some-patient-file.csv"
    )

    result: Dict[
        str, Optional[datetime.datetime]
    ] = catalog.get_last_processed_dates_for_resources(
        data_source=data_source, environment=HelixEnvironment.PRODUCTION
    )
    assert result[people_resource.name] == datetime.datetime(2021, 11, 11)


def test_catalog_get_resource_last_processed_date_for_multiple_segments() -> None:
    clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    catalog.update_resource_last_processed_date_segment(
        "2095895",
        datetime.datetime.strptime("2021-11-11", "%Y-%m-%d"),
        data_source,
        HelixEnvironment.PRODUCTION,
    )
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed = people_resource.last_processed
    assert last_processed is not None
    assert (
        last_processed.get_last_processed(HelixEnvironment.PRODUCTION)
        == "data/events/2095895/2021/11/11/full_day/some-patient-file.csv"
    )

    result: Dict[
        str, Optional[datetime.datetime]
    ] = catalog.get_last_processed_dates_for_resources(
        data_source=data_source, environment=HelixEnvironment.PRODUCTION
    )
    assert result[people_resource.name] == datetime.datetime(2021, 11, 11)


def test_catalog_get_resource_last_processed_date_for_folders() -> None:
    # clean_test_folder()
    repo = DirectoryRepo(location="")
    catalog = Catalog(repo=repo)
    data_source = catalog.get_data_source(
        "catalog/events/mixpanel/events_parquet.json", HelixEnvironment.PRODUCTION
    )
    assert data_source is not None
    assert data_source is not None
    people_resource = data_source.resources[0]
    assert people_resource is not None
    last_processed = people_resource.last_processed
    assert last_processed is not None
    result: List[str] = catalog.get_resource_unprocessed_directories(
        people_resource.name,
        data_source=data_source,
        environment=HelixEnvironment.PRODUCTION,
    )

    assert result[0] == "data/events/2095895/2021/10/02"
    assert result[1] == "data/events/2095895/2021/10/03"

    assert len(result) == 2

import datetime
import functools
import logging
from typing import Literal, Any

from affinity_sync.clients import affinity_base
from . import clients, reader
from .module_types import affinity_v1_api as affinity_types
from .module_types import affinity_v2_api as affinity_types_v2


class CannotDetermineCorrectEntityError(Exception):
    pass


class FieldNotFoundError(Exception):
    pass


FieldType = affinity_types.Location | list[str] | float | str | None | datetime.datetime | list[int]


def insert_entitlement_after(func):
    @functools.wraps(func)
    def wrapper(self: 'Writer', *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.insert_call_entitlement()
        return result

    return wrapper


class Writer:
    __logger = logging.getLogger('affinity_sync.Writer')

    def __init__(
            self,
            affinity_api_key: str,
            db_host: str,
            db_port: int,
            db_name: str,
            db_user: str,
            db_password: str,
    ):
        self.__affinity_v1 = clients.AffinityClientV1(api_key=affinity_api_key)
        self.__affinity_v2 = clients.AffinityClientV2(api_key=affinity_api_key)
        self.__reader = reader.Reader(
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password
        )
        self.__postgres_client = clients.PostgresClient(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        self.__list_fields: dict[int, dict[str, tuple[affinity_types_v2.FieldMetadata, affinity_types.Field]]] = {}

    def insert_call_entitlement(self):
        self.__postgres_client.insert_call_entitlement(entitlement=self.__affinity_v1.api_call_entitlement)

    @functools.cached_property
    def __v1_fields(self) -> list[affinity_types.Field]:
        return self.__affinity_v1.fetch_fields()

    @functools.cached_property
    def __fields(self) -> dict[str, tuple[affinity_types_v2.FieldMetadata, affinity_types.Field]]:
        self.__logger.info('Fetching person fields')
        v1_fields = {field.id: field for field in self.__v1_fields}

        out = {}

        for field in list(self.__affinity_v2.get_people_fields()) + list(self.__affinity_v2.get_company_fields()):
            is_custom = field.type in ['global', 'list']
            is_entriched = field.type == 'enriched'

            if not is_custom and not is_entriched:
                continue

            v1_id = int(field.affinity_id.split('-')[1]) if is_custom else field.affinity_id
            v1_field = v1_fields.get(v1_id)

            if v1_field is None:
                for k, v in v1_fields.items():
                    if v.name == field.name:
                        v1_field = v
                        break

            out[field.name.upper()] = (field, v1_field)

        return out

    def get_list_fields(self, list_id: int) -> dict[str, tuple[affinity_types_v2.FieldMetadata, affinity_types.Field]]:
        if list_fields := self.__list_fields.get(list_id):
            return list_fields

        self.__logger.info(f'Fetching list fields - {list_id}')
        v1_fields = {field.id: field for field in self.__v1_fields}

        out = {}

        for field in list(self.__affinity_v2.get_list_fields(list_id=list_id)):

            if field.type not in ['global', 'list'] or field.affinity_id in ['persons', 'companies']:
                continue

            v1_id = int(field.affinity_id.split('-')[1]) if '-' in field.affinity_id else field.affinity_id
            v1_field = v1_fields.get(v1_id)

            out[field.name.upper()] = (field, v1_field)

        self.__list_fields[list_id] = out

        return out

    def __get_field(
            self,
            field_name: str,
            list_id: int | None = None
    ) -> tuple[affinity_types_v2.FieldMetadata, affinity_types.Field]:
        fields = self.__fields

        if list_id:
            fields = fields | self.get_list_fields(list_id=list_id)

        field = fields.get(field_name.upper())

        if not field:
            raise FieldNotFoundError(f'Field not found - {field_name}')

        return field

    @staticmethod
    def __check_field_value_type(value: FieldType, value_type: affinity_types_v2.FieldValueTypes) -> None:
        if not affinity_types.FieldTypeMap.get(value_type):
            raise ValueError(f'Invalid field value type - {value_type}')

        if not isinstance(value, affinity_types.FieldTypeMap[value_type]) and value is not None:
            raise ValueError(
                f'Field value type mismatch - {value} must be of type {affinity_types.FieldTypeMap[value_type]}'
            )

    @insert_entitlement_after
    def find_or_create_person(
            self,
            first_name: str,
            last_name: str,
            emails: list[str],
            organization_ids: list[int] | None = None,
            cached_field_name: str | None = None,
            cached_filed_value: Any | None = None,
    ) -> affinity_types.Person:
        self.__logger.info(f'Finding or creating person - {first_name} {last_name}')

        if cached_field_name and not cached_filed_value or not cached_field_name and cached_filed_value:
            raise ValueError('Both cached_field_name and cached_filed_value must be provided to use cached lookup')

        if cached_field_name:
            self.__logger.info(f'Finding person by cached field - {cached_field_name} - {cached_filed_value}')
            stale_person_id = self.__reader.get_people_ids_by_field(
                field_name=cached_field_name,
                field_values=[cached_filed_value]
            )

            if len(stale_person_id) == 1:
                self.__logger.info(f'Person found by cached field - {cached_field_name} - {cached_filed_value}')

                try:
                    return self.__affinity_v1.find_person_by_id(person_id=stale_person_id[0])

                except affinity_base.TryAgainError:
                    self.__logger.info('Person must have been deleted')

        organization_ids = organization_ids or []

        person = self.__affinity_v1.find_person_by_emails(emails=emails)

        if person:
            return person

        return self.__affinity_v1.create_person(
            new_person=affinity_types.NewPerson(
                first_name=first_name,
                last_name=last_name,
                emails=emails,
                organization_ids=organization_ids
            )
        )

    @insert_entitlement_after
    def find_company(self, domain: str, linkedin_url: str) -> affinity_types.Company | None:
        self.__logger.info(f'Finding company - {domain} - {linkedin_url}')
        company = self.__affinity_v1.find_company_by_domain(domain=domain, take_best_match=True)

        if company:
            return company

        ids = self.__reader.get_company_ids_by_field('LinkedIn URL', [linkedin_url])

        if len(ids) == 1:
            return self.__affinity_v1.find_company_by_id(ids[0])

        return None

    @insert_entitlement_after
    def create_company(self, name: str, domain: str) -> affinity_types.Company:
        self.__logger.info(f'Creating company - {name} - {domain}')

        return self.__affinity_v1.create_company(
            new_company=affinity_types.NewCompany(
                name=name,
                domain=domain,
                person_ids=[]
            )
        )

    @insert_entitlement_after
    def find_or_create_company(
            self,
            name: str,
            domain: str | None,
            take_best_match: bool = False,
            match_on_name: bool = False,
            cached_field_name: str | None = None,
            cached_filed_value: Any | None = None
    ) -> affinity_types.Company:
        self.__logger.info(f'Finding or creating company - {name}')
        company = None

        if cached_field_name and not cached_filed_value or not cached_field_name and cached_filed_value:
            raise ValueError('Both cached_field_name and cached_filed_value must be provided to use cached lookup')

        if cached_field_name:
            self.__logger.info(f'Finding company by cached field - {cached_field_name} - {cached_filed_value}')
            stale_company_id = self.__reader.get_company_ids_by_field(
                field_name=cached_field_name,
                field_values=[cached_filed_value]
            )

            if len(stale_company_id) == 1:
                self.__logger.info(f'Company found by cached field - {cached_field_name} - {cached_filed_value}')

                try:
                    return self.__affinity_v1.find_company_by_id(company_id=stale_company_id[0])

                except affinity_base.TryAgainError:
                    self.__logger.info('Company must have been deleted')

        if domain:
            company = self.__affinity_v1.find_company_by_domain(domain=domain, take_best_match=take_best_match)

        if company:
            self.__logger.info(f'Company found by domain - {domain}')
            return company

        if match_on_name:
            company = self.__affinity_v1.find_company_by_name(name=name, take_best_match=take_best_match)

            if company:
                self.__logger.info(f'Company found by name - {name}')
                return company

        return self.__affinity_v1.create_company(
            new_company=affinity_types.NewCompany(
                name=name,
                domain=domain,
                person_ids=[]
            )
        )

    @insert_entitlement_after
    def find_or_create_opportunity(
            self,
            name: str,
            list_id: int,
            company_ids: list[int],
            person_ids: list[int],
    ) -> affinity_types.Opportunity:
        self.__logger.info(f'Finding or creating opportunity - {name}')
        opportunity = self.__affinity_v1.find_opportunity_by_name(name=name, list_id=list_id)

        self.__logger.info(f'Opportunity found by name - {name} - {opportunity}')

        if opportunity:
            return opportunity

        self.__logger.info(f'Creating opportunity - {name} - {list_id} - {company_ids} - {person_ids}')

        return self.__affinity_v1.create_opportunity(
            new_opportunity=affinity_types.NewOpportunity(
                name=name,
                list_id=list_id,
                organization_ids=company_ids,
                person_ids=person_ids
            )
        )

    @insert_entitlement_after
    def create_list_entry(
            self,
            entity_id: int,
            list_id: int,
    ) -> affinity_types.ListEntry:
        self.__logger.info(f'Creating list entry - {entity_id} - {list_id}')
        return self.__affinity_v1.create_list_entry(entity_id=entity_id, list_id=list_id)

    @insert_entitlement_after
    def find_list_entry(
            self,
            entity_id: int,
            entity_type: Literal['person', 'company', 'opportunity'],
            list_id: int,
            qualifiers: dict[str, str] | None = None
    ) -> affinity_types.ListEntry | None:
        self.__logger.info(f'Finding list entry - {entity_id} - {list_id}')
        entries = self.__affinity_v1.fetch_all_list_entries(list_id=list_id)
        mathing_entries = [entry for entry in entries if entry.entity_id == entity_id]

        self.__logger.info(f'Found {len(mathing_entries)} entries for entity - {entity_id}')

        if mathing_entries and qualifiers:
            still_matching_entries = []

            for entry in mathing_entries:
                match = True
                current_field_values = self.__affinity_v1.fetch_field_values(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    list_entry_id=entry.id
                )

                for field_name, desired_field_value in qualifiers.items():
                    field, v1_field = self.__get_field(field_name=field_name, list_id=list_id)
                    desired_field_value = desired_field_value \
                        if isinstance(desired_field_value, list) else [desired_field_value]
                    current_field_values = [
                        value.value
                        for value in current_field_values
                        if value.field_id == v1_field.id
                    ]
                    missing_values = [value for value in desired_field_value if value not in current_field_values]
                    extra_values = [value for value in current_field_values if value not in desired_field_value]

                    if missing_values or extra_values:
                        match = False
                        break

                if match:
                    still_matching_entries.append(entry)

            mathing_entries = still_matching_entries

        if len(mathing_entries) > 1:
            raise ValueError(f'Multiple entries found for entity - {entity_id} with qualifiers - {qualifiers}')

        if mathing_entries:
            return mathing_entries[0]

        return None

    @insert_entitlement_after
    def find_or_create_list_entry(
            self,
            entity_id: int,
            entity_type: Literal['person', 'company', 'opportunity'],
            list_id: int,
            qualifiers: dict[str, str] | None = None
    ) -> affinity_types.ListEntry:
        current_entry = self.find_list_entry(
            entity_id=entity_id,
            entity_type=entity_type,
            list_id=list_id,
            qualifiers=qualifiers
        )

        if current_entry:
            return current_entry

        return self.__affinity_v1.create_list_entry(entity_id=entity_id, list_id=list_id)

    @insert_entitlement_after
    def update_person(self, person_id: int, new_person: affinity_types.NewPerson) -> affinity_types.Person:
        self.__logger.info(f'Updating person - {person_id}')
        return self.__affinity_v1.update_person(person_id=person_id, new_person=new_person)

    @insert_entitlement_after
    def update_company(self, company_id: int, new_company: affinity_types.NewCompany) -> affinity_types.Company:
        self.__logger.info(f'Updating company - {company_id}')
        return self.__affinity_v1.update_company(company_id=company_id, new_company=new_company)

    @insert_entitlement_after
    def update_opportunity(
            self,
            opportunity_id: int,
            name: str,
            person_ids: list[int],
            organization_ids: list[int],
    ) -> affinity_types.Opportunity:
        self.__logger.info(f'Updating opportunity - {opportunity_id}')
        return self.__affinity_v1.update_opportunity(
            opportunity_id=opportunity_id,
            name=name,
            person_ids=person_ids,
            organization_ids=organization_ids,
        )

    def current_field_values(
            self,
            field_names: list[str],
            entity_id: int,
            entity_type: Literal['person', 'company', 'opportunity'],
            list_entry_id: int | None = None,
            list_id: int | None = None
    ) -> dict[str, list[affinity_types.FieldValue]]:
        field_names = [field_name.upper() for field_name in field_names]
        current_values = self.__affinity_v1.fetch_field_values(
            entity_id=entity_id,
            entity_type=entity_type,
            list_entry_id=list_entry_id
        )

        out = {}

        for name in field_names:
            field, v1_field = self.__get_field(field_name=name, list_id=list_id)
            out[name] = [value for value in current_values if value.field_id == v1_field.id]

        return out

    def __update_field(
            self,
            entity_id: int,
            list_entry_id: int | None,
            field_name: str,
            field_value: FieldType,
            current_values: list[affinity_types.FieldValue],
            overwrite: bool,
            list_id: int | None,
            status_field: affinity_types.Field | None = None
    ) -> None:
        self.__logger.debug(f'Updating field - {field_name} - {field_value}')
        field, v1_field = self.__get_field(field_name=field_name, list_id=list_id)
        self.__check_field_value_type(value=field_value, value_type=field.value_type)

        if field_name.upper() == 'STATUS' and status_field:
            self.__logger.info(f'Updating status field - {field_value}')
            options = status_field.dropdown_options
            correct_option = next((option for option in options if option.text.upper() == field_value.upper()), None)

            if not correct_option:
                raise ValueError(f'Invalid status value - {field_value}')

            field_value = correct_option.id

        current_values = [value for value in current_values if value.field_id == v1_field.id]
        current_raw_values = [value.value for value in current_values]

        if current_values and not overwrite:
            self.__logger.info('Field already exists - will not overwrite')
            return

        if not v1_field.allows_multiple and isinstance(field_value, list):
            raise ValueError(f'Field does not allow multiple values - {field_name}')

        if not isinstance(field_value, list):
            field_value = [field_value]

        field_value = list(filter(None, field_value))

        is_date_field = isinstance(next(iter(field_value), None), datetime.datetime)

        if is_date_field:
            current_raw_values = [value.value.split('.')[0] for value in current_values]
            field_value = [value.replace(tzinfo=None).strftime('%Y-%m-%dT%H:%M:%S') for value in field_value]

        values_to_remove = {
            value.id for value in current_values
            if (value.value.split('.')[0] if is_date_field else value.value) not in field_value
        }
        values_to_add = [value for value in field_value if value not in current_raw_values]

        if not values_to_remove and not values_to_add:
            self.__logger.info('No changes required')
            return

        for value_id in values_to_remove:
            self.__logger.info(f'Removing field value - {value_id}')
            self.__affinity_v1.delete_field_value(field_value_id=value_id)

        for value in values_to_add:
            self.__logger.info(f'Adding field value - {value}')
            self.__affinity_v1.create_field_value(
                field_id=v1_field.id,
                entity_id=entity_id,
                value=value.model_dump() if isinstance(value, affinity_types.Location) else value,
                list_entry_id=list_entry_id if v1_field.list_id else None
            )

    @insert_entitlement_after
    def update_fields(
            self,
            entity_id: int,
            entity_type: Literal['person', 'company', 'opportunity'],
            fields: dict[str, FieldType],
            list_entry_id: int | None = None,
            list_id: int | None = None,
            overwrite: bool = True
    ) -> None:
        self.__logger.info(f'Updating fields - {len(fields)}')

        if entity_type == 'opportunity' and list_entry_id is None:
            raise CannotDetermineCorrectEntityError('List entry id is required for opportunities')

        if list_entry_id is not None and list_id is None:
            raise ValueError('list_id is required when list_entry_id is provided')

        if list_id is not None and list_entry_id is None:
            raise ValueError('list_entry_id is required when list_id is provided')

        self.__logger.info(f'Updating fields - {len(fields)}')

        current_values = self.__affinity_v1.fetch_field_values(
            entity_id=entity_id,
            entity_type=entity_type,
        )

        if list_entry_id:
            current_values += self.__affinity_v1.fetch_field_values(
                entity_id=entity_id,
                entity_type=entity_type,
                list_entry_id=list_entry_id
            )

        status_field = None

        if any(field_name.upper() == 'STATUS' for field_name in fields.keys()):
            options = self.__affinity_v1.fetch_fields()
            status_field = next((
                field for field in options
                if field.name.upper() == 'STATUS' and list_id == field.list_id
            ), None)

        for field_name, field_value in fields.items():
            self.__update_field(
                entity_id=entity_id,
                field_name=field_name,
                field_value=field_value,
                current_values=current_values,
                list_entry_id=list_entry_id,
                list_id=list_id,
                overwrite=overwrite,
                status_field=status_field
            )

    @insert_entitlement_after
    def add_file_to_company_if_not_exists(self, company_id: int, file_name: str, file: bytes, file_type: str) -> None:
        self.__logger.info(f'Adding file to company - {company_id} - {file_name}')
        existing_files = self.__affinity_v1.fetch_all_entity_files(entity_id=company_id, entity_type='company')

        if file_name in [file.name for file in existing_files]:
            self.__logger.info('File already exists - will not add again')
            return

        self.__affinity_v1.add_file_to_entity(
            entity_id=company_id,
            entity_type='company',
            file_name=file_name,
            file=file,
            file_type=file_type
        )

    @insert_entitlement_after
    def add_note_to_entity(
            self,
            entity_id: int,
            entity_type: Literal['person', 'company', 'opportunity'],
            note: str,
            creator_id: int
    ) -> affinity_types.Note:
        self.__logger.info(f'Adding note to entity - {entity_id} - {entity_type}')
        return self.__affinity_v1.add_note_to_entity(
            entity_id=entity_id,
            entity_type=entity_type,
            note=note,
            creator_id=creator_id
        )

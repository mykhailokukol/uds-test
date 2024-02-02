from config.database import create_query


if __name__ == "__main__":
    # Create table named files
    create_query(
        """
        create sequence if not exists files_id_seq;
        
        create table if not exists files
        (
            id bigint not null default nextval('files_id_seq'),
            filepath character varying(255) not null,
            name character varying(255) not null,
            size integer not null,
            updated_at timestamp,
            
            constraint files_pkey primary key (id)
        );
        
        alter sequence files_id_seq owned by public.files.id
        """
    )

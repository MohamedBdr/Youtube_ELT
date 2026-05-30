
import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur, conn, schema, row):
    try:
        if schema == "staging":
            cur.execute(f'''
                INSERT INTO {schema}.{table}
                ("video_id", "video_title", "upload_date", "duration", "video_views", "likes_count", "comments_count")
                VALUES (
                    %(video_id)s,
                    %(title)s,
                    %(publishedAt)s,
                    %(duration)s,
                    %(viewCount)s,
                    %(likeCount)s,
                    %(commentCount)s
                );
            ''', row)

        else:
            cur.execute(f'''
                INSERT INTO {schema}.{table}
                ("video_id", "video_title", "upload_date", "duration", "video_views", "likes_count", "comments_count")
                VALUES (
                    %(video_id)s,
                    %(video_title)s,
                    %(upload_date)s,
                    %(duration)s,
                    %(video_views)s,
                    %(likes_count)s,
                    %(comments_count)s
                );
            ''', row)

        conn.commit()

    except Exception as e:
        logger.error(f"Insert error video_id={row.get('video_id')}: {e}")
        raise
    
def update_rows(cur, conn, schema, row):

    try:
        # staging
        if schema == "staging":
            video_id = 'video_id'
            video_title = 'title'
            upload_date = 'publishedAt'
            duration = 'duration'
            video_views = 'viewCount'
            likes_count = 'likeCount'
            comments_count = 'commentCount'
        # Core
        else:
            video_id = 'video_id'
            video_title = 'video_title'
            upload_date = 'upload_date'
            duration = 'duration'
            video_views = 'video_views'
            likes_count = 'likes_count'
            comments_count = 'comments_count'
        
        cur.execute(f'''
            UPDATE {schema}.{table}
            SET
                "video_title" = %({video_title})s,
                "video_views" = %({video_views})s,
                "likes_count" = %({likes_count})s,
                "comments_count" = %({comments_count})s
            WHERE
                "video_id" = %({video_id})s
                AND "upload_date" = %({upload_date})s;
            ''', row)

        conn.commit()
        logger.info(f"Update row with video_id: {row['video_id']}")

    except Exception as e:
        logger.error(f"Error updating row with video_id: {row['video_id']} - {e}")
        raise e

def delete_rows(cur, conn, schema, ids_to_delete):
    try:
        ids_to_delete = f"""({", ".join(f"'{id}'" for id in ids_to_delete)})"""

        cur.execute(
            f'''
            DELETE FROM {schema}.{table}
            WHERE "video_id" IN {ids_to_delete}
        '''
        )

        conn.commit()
        logger.info(f"Update row with video_id: {ids_to_delete}")

    except Exception as e:
        logger.error(f"Error updating row with video_id: {ids_to_delete} - {e}")
        raise e



